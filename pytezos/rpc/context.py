from pytezos.rpc.node import Node
from pytezos.rpc.contract import Contract


class Context:

    def __init__(self, block_id='head', chain_id='main', node=Node()):
        self._block_id = block_id
        self._chain_id = chain_id
        self._node = node
        self._path = f'chains/{chain_id}/blocks/{block_id}/context/raw/json'

    def __repr__(self):
        return self._path

    def __call__(self, *args, **kwargs):
        return self._node.get(self._path)

    def get_contract(self, public_key_hash) -> Contract:
        return Contract(public_key_hash, self._block_id, self._chain_id, self._node)
