from pprint import pformat

from pytezos.rpc.node import Node
from pytezos.rpc.contract import Contract


class Context:

    def __init__(self, block_id='head', node=Node()):
        self._block_id = block_id
        self._node = node
        self._context = dict()
        self._synced = False

    def _sync(self):
        if self._block_id == 'head' or not self._synced:
            self._context = self._node.get(
                f'chains/{self._node.chain_id}/blocks/{self._block_id}/context/raw/json?depth=1')
            self._synced = True

    def to_dict(self) -> dict:
        self._sync()
        return self._context

    def __repr__(self):
        return pformat(self.to_dict(), compact=True)

    def __getitem__(self, item):
        return self.to_dict()[item]

    def __getattr__(self, item):
        return getattr(self.to_dict(), item)

    def get_contract(self, public_key_hash) -> Contract:
        return Contract(public_key_hash, self._block_id, self._node)
