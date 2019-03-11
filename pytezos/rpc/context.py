from functools import lru_cache

from pytezos.rpc.node import RpcQuery


class Contract(RpcQuery):

    def __init__(self, *args, **kwargs):
        super(Contract, self).__init__(
            properties=[
                'balance', 'counter', 'delegatable', 'delegate', 'manager',
                'manager_key', 'script', 'spendable', 'storage'
            ],
            *args, **kwargs)


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
            child_class=Contract,
            **self._kwargs
        )
