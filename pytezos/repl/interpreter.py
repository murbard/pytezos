from pytezos.repl.stack import Stack


def exec_micheline(expression, stack: Stack) -> Stack:
    pass


class ExecutionContext:

    def __init__(self):
        self.stack = Stack()

    def execute(self, node):
        if isinstance(node, dict):
            if node.get('prim'):
                pass
            else:
                pass
        elif isinstance(node, list):
            for child in node:
                self.execute(child)
        else:
            assert False, node
