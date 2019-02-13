from pytezos.rpc.node import Node


class Contract:
    __dyn_attrs__ = ['balance', 'counter', 'delegatable', 'delegate', 'manager', 'manager_key', 'script',
                     'spendable', 'storage']

    def __init__(self, public_key_hash, block_id='head', chain_id='main', node=Node()):
        self._pkh = public_key_hash
        self._block_id = block_id
        self._chain_id = chain_id
        self._node = node
        self._raw = dict()
        self._synced = False
        self._path = f'chains/{self._chain_id}/blocks/{self._block_id}/context/contracts/{self._pkh}'

    def _sync_all(self):
        if 'head' in self._block_id or not self._synced:
            self._raw = self._node.get(self._path)
            self._synced = True

    def _sync_item(self, item):
        if 'head' in self._block_id or item not in self._raw:
            self._raw[item] = self._node.get(f'{self._path}/{item}')

    def to_dict(self) -> dict:
        self._sync_all()
        return self._raw

    def __repr__(self):
        return self._path

    def __dir__(self):
        return sorted(super(Contract, self).__dir__() + self.__dyn_attrs__)

    def __getitem__(self, item):
        if item in self.__dyn_attrs__:
            self._sync_item(item)
        else:
            self._sync_all()
        return self._raw[item]

    def __getattr__(self, item):
        if not item.startswith('_'):
            if item in self.__dyn_attrs__:
                self._sync_item(item)
                return self._raw[item]
            else:
                self._sync_all()
                return getattr(self._raw, item)
        raise AttributeError(item)
