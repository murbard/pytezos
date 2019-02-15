from pytezos.rpc.node import Node


class Contract:
    __dyn_attrs__ = ['balance', 'counter', 'delegatable', 'delegate', 'manager', 'manager_key', 'script',
                     'spendable', 'storage']

    def __init__(self, public_key_hash, block_id='head', chain_id='main', node=Node()):
        self._pkh = public_key_hash
        self._block_id = block_id
        self._chain_id = chain_id
        self._node = node
        self._path = f'chains/{chain_id}/blocks/{block_id}/context/contracts/{public_key_hash}'

    def __repr__(self):
        return self._path

    def __call__(self, *args, **kwargs):
        return self._node.get(self._path)

    def __dir__(self):
        return sorted(super(Contract, self).__dir__() + self.__dyn_attrs__)

    def __getattr__(self, item):
        if item in self.__dyn_attrs__:
            return self._node.get(f'{self._path}/{item}')
        raise AttributeError(item)
