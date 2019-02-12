from datetime import datetime

from pytezos.rpc.node import Node
from pytezos.rpc.block import Block, BlockSelector


class Chain:
    __dyn_attrs__ = ['head', 'genesis']

    def __init__(self, node=Node()):
        self._node = node
        self._blocks = {x: Block(x, node) for x in self.__dyn_attrs__}

    def __dir__(self):
        return sorted(super(Chain, self).__dir__() + self.__dyn_attrs__)

    def __getattr__(self, item):
        if item in self._blocks:
            return self._blocks[item]
        raise AttributeError(item)

    def get_block(self, block_id) -> Block:
        """
        All the information about a block.
        :param block_id: can be block hash (str) or block level (int); special cases: head, genesis
        :return: an instance of Block class
        """
        return Block(block_id, self._node)

    def get_blocks(self, length=1, head: list = None, min_date: datetime = None) -> BlockSelector:
        """
        Lists known heads of the blockchain sorted with decreasing fitness. Optional arguments allows to returns
        the list of predecessors for known heads or the list of predecessors for a given list of blocks.
        :param length: The requested number of predecessors to returns (per requested head)
        :param head: An empty argument requests blocks from the current heads. A non empty list allow to request
        specific fragment of the chain
        :param min_date: When `min_date` is provided, heads with a timestamp before `min_date` are filtered out
        :return: an instance of BlockSelector class
        """
        return BlockSelector(length, head, min_date, self._node)
