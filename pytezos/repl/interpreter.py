from pytezos.michelson.converter import michelson_to_micheline
from pytezos.repl.stack import Stack
from pytezos.repl.control import do_interpret


class Interpreter:

    def __init__(self):
        self.stack = Stack([])

    def run(self, command):
        expr = michelson_to_micheline(command)
        return do_interpret(self.stack, expr)
