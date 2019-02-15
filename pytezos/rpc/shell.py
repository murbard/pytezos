from functools import lru_cache

from pytezos.rpc.node import Node, RpcQuery
from pytezos.rpc.chain import Chain
from pytezos.rpc.block import Block, Context


class Shell(RpcQuery):

    def __init__(self, node=Node()):
        super(Shell, self).__init__(node=node)

    @property
    @lru_cache(maxsize=None)
    def chains(self):
        return RpcQuery(
            path='chains',
            node=self._node,
            sub_class={
                'main': Chain,
                '_default': Chain
            }
        )

    @property
    def main(self) -> Chain:
        return self.chains.main

    @property
    def blocks(self):
        return self.main.blocks

    @property
    def head(self) -> Block:
        return self.main.head

    @property
    def context(self) -> Context:
        return self.head.context
