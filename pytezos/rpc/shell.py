from pytezos.rpc.node import Node
from pytezos.rpc.chain import Chain
from pytezos.rpc.block import Block
from pytezos.rpc.context import Context


class Shell:
    """
    Represents basic level of the RPC API structure
    """

    def __init__(self, node=Node()):
        self._node = node

    def get_chain(self, chain_id='main') -> Chain:
        """
        Returns a specific chain
        :param chain_id: i.e. 'NetXdQprcVkpaWU'
        :return: cached Chain instance
        """
        return Chain(chain_id, self._node)

    @property
    def main(self) -> Chain:
        return self.get_chain('main')

    @property
    def head(self) -> Block:
        return self.main.head

    @property
    def context(self) -> Context:
        return self.main.head.context
