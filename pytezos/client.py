from pytezos.rpc import ShellQuery
from pytezos.crypto import Key
from pytezos.operation.group import OperationGroup
from pytezos.operation.content import ContentMixin


class PyTezosClient(ContentMixin):

    def __init__(self, shell=None, key=None):
        self.shell = shell  # type: ShellQuery
        self.key = key  # type: Key

    @staticmethod
    def using(*args):
        kwargs = dict()
        for arg in args:
            if isinstance(arg, Key):
                kwargs['key'] = arg
            elif isinstance(arg, ShellQuery):
                kwargs['shell'] = arg
            else:
                raise NotImplementedError(arg)
        return PyTezosClient(**kwargs)

    def operation_group(self, protocol=None, branch=None, contents: list = None, signature=None):
        return OperationGroup(
            shell=self.shell,
            key=self.key,
            protocol=protocol,
            branch=branch,
            contents=contents,
            signature=signature
        )

    def operation(self, content: dict):
        return OperationGroup(
            shell=self.shell,
            key=self.key,
            contents=[content]
        )
