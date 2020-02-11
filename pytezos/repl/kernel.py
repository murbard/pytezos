from ipykernel.kernelbase import Kernel

from pytezos.michelson.grammar import MichelsonParserError
from pytezos.michelson.converter import michelson_to_micheline, micheline_to_michelson
from pytezos.repl.stack import Stack, StackItem
from pytezos.repl.control import do_interpret, MichelsonRuntimeError


class MichelsonInterpreter:

    def __init__(self):
        self.stack = Stack([])

    def run(self, code):
        try:
            expr = michelson_to_micheline(code)
        except MichelsonParserError as e:
            return

        backup = self.stack.copy()

        try:
            res = do_interpret(self.stack, expr)
        except MichelsonRuntimeError as e:
            self.stack = backup
            return

        if isinstance(res, StackItem):
            return micheline_to_michelson(res.val_expr)


class MichelsonKernel(Kernel):
    implementation = 'IMichelson'
    implementation_version = '0.1.0'
    language_info = {
        'mimetype': 'text/x-michelson',
        'file_extension': 'tz',
        'codemirror_mode': 'michelson'
    }
    banner = 'Tezos VM language'
    help_links = [
        'https://michelson.nomadic-labs.com/',
        'https://tezos.gitlab.io/whitedoc/michelson.html'
    ]

    def __init__(self, **kwargs):
        super(MichelsonKernel, self).__init__(**kwargs)
        self.interpreter = MichelsonInterpreter()

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        try:
            self.interpreter.run(code)
        except MichelsonRuntimeError:
            pass
        except MichelsonParserError:
            pass
        else:
            pass

        if not silent:
            stream_content = {'name': 'stdout', 'text': code}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {}}

    def do_complete(self, code, cursor_pos):
        pass

    def do_inspect(self, code, cursor_pos, detail_level=0):
        pass
