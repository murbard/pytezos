from datetime import datetime
from typing import List
from functools import lru_cache
from pendulum.parsing.exceptions import ParserError
import pendulum

from pytezos.rpc.node import Node
from pytezos.rpc.block import Block


def to_timestamp(v):
    if isinstance(v, str):
        try:
            v = pendulum.parse(v)
        except ParserError:
            pass
    if isinstance(v, datetime):
        v = int(v.timestamp())
    return v


class Chain:

    def __init__(self, chain_id='main', node=Node()):
        self._chain_id = chain_id
        self._node = node
        self._path = f'chains/{chain_id}'

    def __repr__(self):
        return self._path

    @lru_cache(maxsize=None)
    def get_block(self, block_id) -> Block:
        """
        All the information about a block, cached
        :param block_id: can be block hash (str) or block level (int); special aliases: head, genesis
        :return: cached instance of Block class (non related with internal block cache)
        """
        return Block(block_id, self._chain_id, self._node)

    def get_blocks(self, length=None, head=None, min_date=None) -> List[List[Block]]:
        """
        Lists known heads of the blockchain sorted with decreasing fitness. Optional arguments allows to returns
        the list of predecessors for known heads or the list of predecessors for a given list of blocks.
        :param length: The requested number of predecessors to returns (per requested head)
        :param head: An empty argument requests blocks from the current heads. A non empty list allow to request
        specific fragment of the chain
        :param min_date: When `min_date` is provided, heads with a timestamp before `min_date` are filtered out;
        can be integer, string in ISO8601 format
        :return: a list of lists of Block instances
        """
        hash_matrix = self._node.get(f'{self._path}/blocks', params=dict(
            length=length,
            head=head,
            min_date=to_timestamp(min_date)
        ))
        blocks = [
            list(map(lambda x: Block(x, self._chain_id, self._node), hash_row))
            for hash_row in hash_matrix
        ]
        return blocks

    @property
    @lru_cache(maxsize=None)
    def chain_id(self):
        """
        The chain unique identifier, cached
        :return: base58 encoded string, i.e. 'NetXdQprcVkpaWU'
        """
        return self._node.get(f'{self._path}/chain_id')

    @property
    def head(self) -> Block:
        return self.get_block('head')

    @property
    def genesis(self) -> Block:
        return self.get_block('genesis')
