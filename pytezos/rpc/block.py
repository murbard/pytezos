from functools import lru_cache

from pytezos.rpc.node import RpcQuery, urljoin


class Contract(RpcQuery):

    def __init__(self, *args, **kwargs):
        super(Contract, self).__init__(properties=[
            'balance', 'counter', 'delegatable', 'delegate', 'manager',
            'manager_key', 'script', 'spendable', 'storage'
        ], *args, **kwargs)


class BlockHeader(RpcQuery):

    def __init__(self, *args, **kwargs):
        super(BlockHeader, self).__init__(properties=[
            'shell', 'protocol_data', 'raw'
        ], *args, **kwargs)


class Operation(RpcQuery):

    def __init__(self, *args, **kwargs):
        super(Operation, self).__init__(*args, **kwargs)


class Context(RpcQuery):

    def __init__(self, *args, **kwargs):
        super(Context, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self._node.get(f'{self._path}/raw/json?depth=1', cache=self._cache)

    @property
    @lru_cache(maxsize=None)
    def contracts(self):
        """
        Attention: very slow method
        :return: list of Contracts
        """
        return RpcQuery(
            path=f'{self._path}/contracts',
            node=self._node,
            child_class=Contract
        )


class Block(RpcQuery):

    def __init__(self, *args, **kwargs):
        kwargs['cache'] = 'head' not in kwargs.get('path')
        super(Block, self).__init__(properties={
            'hash': RpcQuery,
            'header': BlockHeader,
            'context': Context,
            'metadata': RpcQuery,
            'operation_hashes': RpcQuery
        }, *args, **kwargs)

    @property
    @lru_cache(maxsize=None)
    def operations(self):
        return RpcQuery(
            path=f'{self._path}/operations',
            node=self._node,
            child_class=Operation
        )

    def freeze(self):
        """
        Returns fixed-hash block, useful for aliases, like head, head~1, etc.
        :return: Block instance with hash initialized
        """
        parent_path, _ = self._path.rsplit('/', maxsplit=1)
        fixed_path = urljoin(parent_path, self.hash())
        return Block(path=fixed_path, node=self._node)
