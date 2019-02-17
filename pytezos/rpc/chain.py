from datetime import datetime
from functools import lru_cache
from pendulum.parsing.exceptions import ParserError
import pendulum

from pytezos.rpc.node import RpcQuery
from pytezos.rpc.block import Block


def to_timestamp(v):
    try:
        v = pendulum.parse(v)
    except ParserError:
        pass
    if isinstance(v, datetime):
        v = int(v.timestamp())
    return v


class Chain(RpcQuery):

    def __init__(self, *args, **kwargs):
        super(Chain, self).__init__(*args, **kwargs)

    @property
    @lru_cache(maxsize=None)
    def blocks(self):
        return RpcQuery(
            path=f'{self._path}/blocks',
            node=self._node,
            child_class=Block,
            properties=['head', 'genesis']
        )

    @property
    def head(self) -> Block:
        return self.blocks.head

    @property
    def genesis(self) -> Block:
        return self.blocks.genesis
