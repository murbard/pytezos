from functools import lru_cache

from pytezos.crypto import Key
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
            child_class=Chain,
            properties=['main']
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

    def get_public_key(self, pkh) -> Key:
        """
        Wrapped public key of the baker
        :param pkh: public key hash, base58 encoded, like 'tz1eKkWU5hGtfLUiqNpucHrXymm83z3DG9Sq'
        :return: Key instance
        """
        pk = self.context.contracts[pkh].manager_key()['key']
        return Key(pk)
