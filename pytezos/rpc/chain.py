from functools import lru_cache
from typing import List
import os

from pytezos.rpc.node import RpcQuery
from pytezos.rpc.block import Block, BlockListList
from pytezos.rpc.operation import Operation


class OperationsDict(RpcQuery):

    def _get_operations_list(self, key, kind=None):
        operations = self.get(key)

        if kind:
            if isinstance(kind, str):
                kind = {kind}
            elif isinstance(kind, list):
                kind = set(kind)

            operations = filter(
                lambda op: any(map(
                    lambda x: x['kind'] in kind, op['contents'])), operations)

        return list(map(
            lambda x: Operation(data=x, node=self._node, **self._kwargs),
            operations
        ))

    def applied(self, kind=None) -> List[Operation]:
        """
        :param kind: endorsement, seed_nonce_revelation, double_endorsement_evidence, double_baking_evidence,
        activate_account, proposals, ballot, reveal, transaction, origination, delegation
        :return:
        """
        return self._get_operations_list('applied', kind=kind)

    def refused(self) -> List[Operation]:
        return self._get_operations_list('refused')

    def branch_delayed(self) -> List[Operation]:
        return self._get_operations_list('branch_delayed')

    def unprocessed(self) -> List[Operation]:
        return self._get_operations_list('unprocessed')


class Mempool(RpcQuery):

    def __init__(self, *args, **kwargs):
        super(Mempool, self).__init__(
            properties={'pending_operations': OperationsDict},
            *args, **kwargs)

    @property
    def filter(self, **kwargs):
        """
        minimal_fees, minimal_nanotez_per_gas_unit, minimal_nanotez_per_byte
        :return:
        """
        if kwargs:
            return self._node.post(f'{self._path}/filter', json=kwargs)
        return self._node.get(f'{self._path}/filter')


class Chain(RpcQuery):

    def __init__(self, *args, **kwargs):
        kwargs.update(
            chain_id=os.path.basename(kwargs.get('path', ''))
        )
        super(Chain, self).__init__(
            properties={'mempool': Mempool},
            *args, **kwargs)

    @property
    @lru_cache(maxsize=None)
    def blocks(self):
        return BlockListList(
            path=f'{self._path}/blocks',
            node=self._node,
            child_class=Block,
            properties=['head', 'genesis'],
            **self._kwargs
        )

    @property
    def head(self) -> Block:
        return self.blocks.head

    @property
    def genesis(self) -> Block:
        return self.blocks.genesis
