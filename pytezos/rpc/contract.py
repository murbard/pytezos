from pytezos.rpc.node import Node


class Contract:
    __dyn_attrs__ = []

    def __init__(self, public_key_hash, block_id='head', node=Node()):
        self._pkh = public_key_hash
        self._block_id = block_id
        self._node = node
        self._contract = dict()
        self._synced = False

    def _sync_all(self):
        if self._block_id == 'head' or not self._synced:
            self._contract = self._node.get(
                f'chains/{self._node.chain_id}/blocks/{self._block_id}/context/contracts/{self._pkh}')
            self._synced = True

    def _sync_item(self, item):
        if self._block_id == 'head' or item not in self._contract:
            self._contract[item] = self._node.get(
                f'chains/{self._node.chain_id}/blocks/{self._block_id}/context/contracts/{self._pkh}/{item}')

    def to_dict(self):
        self._sync_all()
        return self._contract
