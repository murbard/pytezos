import yaml
from copy import deepcopy
from ipykernel.kernelbase import Kernel
from tabulate import tabulate
from pprint import pformat

from pytezos.michelson.grammar import MichelsonParserError, MichelsonParser
from pytezos.michelson.converter import michelson_to_micheline, micheline_to_michelson
from pytezos.repl.control import do_interpret, MichelsonRuntimeError
from pytezos.repl.helpers import *
from pytezos.repl.arithmetic import *
from pytezos.repl.structures import *


def is_stack(result):
    if isinstance(result, StackItem):
        return True
    elif isinstance(result, list):
        return all(map(lambda x: isinstance(x, StackItem), result))
    else:
        return False


def parse_rows(result):
    if not isinstance(result, list):
        result = [result]

    def make_row(item: StackItem):
        row = {
            'value_expression': micheline_to_michelson(item.val_expr),
            'type_expression': micheline_to_michelson(item.type_expr)
        }
        if item.val_annot is not None:
            row['value_annotation'] = item.val_annot
        return row

    return list(map(make_row, result))


def format_table(rows, execution_count):
    return {
        'data': {
            'text/plain': tabulate(rows, tablefmt='simple'),
            'text/html': tabulate(rows, tablefmt='html'),
        },
        'metadata': {},
        'execution_count': execution_count
    }


def format_text(text, execution_count):
    return {
        'data': {
            'text/plain': text,
        },
        'metadata': {},
        'execution_count': execution_count
    }


def parse_error(error) -> tuple:
    ename = type(error).__name__
    if isinstance(error, MichelsonRuntimeError):
        evalue, traceback = error.message, ['at ' + ' -> '.join(error.trace)]
    elif isinstance(error, MichelsonParserError):
        evalue, traceback = error.message, [f'at line {error.line}, pos {error.pos}']
    else:
        evalue, traceback = pformat(error.args, compact=True), []
    return ename, evalue, [f'{ename}: {evalue}'] + traceback


class MichelsonKernel(Kernel):
    implementation = 'IMichelson'
    implementation_version = '0.1.0'
    language_info = {
        'name': 'Michelson',
        'mimetype': 'text/x-michelson',
        'file_extension': 'tz',
        'codemirror_mode': 'michelson'
    }
    banner = 'Michelson (Tezos VM language)'
    help_links = [
        'https://michelson.nomadic-labs.com/',
        'https://tezos.gitlab.io/whitedoc/michelson.html'
    ]

    def __init__(self, **kwargs):
        super(MichelsonKernel, self).__init__(**kwargs)
        self.stack = Stack([])
        self.parser = MichelsonParser(extra_primitives=helpers_prim)

    def send_error(self, error):
        ename, evalue, traceback = parse_error(error)
        self.send_response(self.iopub_socket, 'stream', {'name': 'stderr', 'text': '\n'.join(traceback)})
        return {
            'status': 'error',
            'execution_count': self.execution_count,
            'ename': ename,
            'evalue': evalue,
            'traceback': traceback
        }

    def send_result(self, silent=False, result=None):
        if not silent and result is not None:
            if is_stack(result):
                rows = parse_rows(result)
                self.send_response(self.iopub_socket, 'display_data', format_table(rows, self.execution_count))
            else:
                text = micheline_to_michelson(result)
                self.send_response(self.iopub_socket, 'execute_result', format_text(text, self.execution_count))
        return {
            'status': 'ok',
            'execution_count': self.execution_count
        }

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        try:
            code_expr = michelson_to_micheline(code, parser=self.parser)
        except MichelsonParserError as e:
            return self.send_error(e)

        backup = deepcopy(self.stack)

        try:
            res = do_interpret(self.stack, code_expr)
        except MichelsonRuntimeError as e:
            self.stack = backup
            return self.send_error(e)

        return self.send_result(silent, res)

    def do_complete(self, code, cursor_pos):
        pass

    def do_inspect(self, code, cursor_pos, detail_level=0):
        pass
