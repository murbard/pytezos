import os

from pytezos.rpc.node import RpcQuery
from pytezos.rpc.block import Block, BlockListListQuery
from pytezos.rpc.operation import OperationsDict


class MempoolFilterQuery(RpcQuery):

    def post(self, configuration):
        """
        :param configuration: a JSON dictionary, known keys are `minimal_fees`, `minimal_nanotez_per_gas_unit`,
        `minimal_nanotez_per_byte`
        """
        return self._node.post(
            path=self._path,
            json=configuration
        )


class InvalidBlockQuery(RpcQuery):

    def delete(self):
        return self._node.delete(self._path)


class ChainQuery(RpcQuery):

    def __init__(self, *args, **kwargs):
        kwargs.update(
            chain_id=os.path.basename(kwargs.get('path', ''))
        )
        super(ChainQuery, self).__init__(
            properties=['chain_id', 'checkpoint'],
            *args, **kwargs)

    @property
    def blocks(self):
        return BlockListListQuery(
            path=f'{self._path}/blocks',
            node=self._node,
            child_class=Block,
            properties=['head', 'genesis'],
            **self._kwargs
        )

    @property
    def invalid_blocks(self):
        return RpcQuery(
            path=f'{self._path}/invalid_blocks',
            node=self._node,
            child_class=InvalidBlockQuery,
            **self._kwargs
        )

    @property
    def mempool(self):
        return RpcQuery(
            path=f'{self._path}/mempool',
            node=self._node,
            properties={
                'pending_operations': OperationsDict,
                'filter': MempoolFilterQuery
            },
            **self._kwargs
        )


class ChainsQuery(RpcQuery):

    def __init__(self, *args, **kwargs):
        super(ChainsQuery, self).__init__(
            child_class=ChainQuery,
            properties=['main', 'test'],
            *args, **kwargs
        )
