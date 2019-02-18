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

    def get_public_key(self, pkh) -> str:
        """
        Public key by the public key hash
        :param pkh: public key hash, base58 encoded, i.e. 'tz1eKkWU5hGtfLUiqNpucHrXymm83z3DG9Sq'
        :return: base58 encoded public key
        """
        if pkh.startswith('KT1'):  # it is not pkh, but let's handle this
            pkh = self.context.contracts[pkh].manager_key().get('manager')

        pk = self.context.contracts[pkh].manager_key().get('key')
        if not pk:
            raise ValueError('Public key is not revealed')

        return pk
