from pytezos.rpc.node import Node
from pytezos.rpc.contract import Contract


class Context:

    def __init__(self, block_id='head', chain_id='main', node=Node()):
        self._block_id = block_id
        self._chain_id = chain_id
        self._node = node
        self._raw = dict()
        self._synced = False
        self._path = f'chains/{chain_id}/blocks/{block_id}/context'

    def _sync(self):
        if 'head' in self._block_id or not self._synced:
            self._raw = self._node.get(f'{self._path}/raw/json?depth=1')
            self._synced = True

    def to_dict(self) -> dict:
        self._sync()
        return self._raw

    def __repr__(self):
        return self._path

    def __getitem__(self, item):
        return self.to_dict()[item]

    def __getattr__(self, item):
        if not item.startswith('_'):
            return getattr(self.to_dict(), item)
        raise AttributeError(item)

    def get_contract(self, public_key_hash) -> Contract:
        return Contract(public_key_hash, self._block_id, self._chain_id, self._node)
