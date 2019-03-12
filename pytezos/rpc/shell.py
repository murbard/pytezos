from functools import lru_cache

from pytezos.rpc.node import Node, RpcQuery
from pytezos.rpc.chain import Chain, OperationsDict, Mempool
from pytezos.rpc.block import Block
from pytezos.rpc.context import Context
from pytezos.rpc.helpers import HelpersMixin
from pytezos.rpc.protocol import Protocol


class Shell(RpcQuery, HelpersMixin):

    def __init__(self, node=Node()):
        super(Shell, self).__init__(node=node)

    @property
    @lru_cache(maxsize=None)
    def chains(self):
        return RpcQuery(
            path='chains',
            node=self._node,
            child_class=Chain,
            properties=['main']
        )

    @property
    def main(self) -> Chain:
        return self.chains.main

    @property
    def test(self) -> Chain:
        return self.chains.test

    @property
    def blocks(self):
        return self.main.blocks

    @property
    def head(self) -> Block:
        return self.main.head

    @property
    def context(self) -> Context:
        return self.head.context

    @property
    def mempool(self) -> Mempool:
        return self.main.mempool

    @property
    def pending_operations(self) -> OperationsDict:
        return self.main.mempool.pending_operations

    @property
    def protocols(self):
        return RpcQuery(
            path='protocols',
            node=self._node,
            child_class=Protocol
        )

    def level(self) -> int:
        return self.head.level()

    def cycle(self) -> int:
        return self.head.cycle()
