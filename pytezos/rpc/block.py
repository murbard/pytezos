from functools import lru_cache

from pytezos.rpc.node import Node
from pytezos.rpc.context import Context
from pytezos.encoding import base58_decode, scrub_input


class Block:
    __dyn_attrs__ = ['hash', 'header', 'metadata', 'operations']

    def __init__(self, block_id='head', chain_id='main', node=Node()):
        self._block_id = block_id
        self._chain_id = chain_id
        self._node = node
        self._raw = dict()
        self._synced = False
        self._path = f'chains/{chain_id}/blocks/{block_id}'

        try:
            base58_decode(scrub_input(block_id))
            self._raw['hash'] = block_id
        except ValueError:
            pass

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

    def __dir__(self):
        return sorted(super(Block, self).__dir__() + self.__dyn_attrs__)

    def __repr__(self):
        return self._path

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

    @property
    @lru_cache(maxsize=None)
    def context(self) -> Context:
        return Context(self._block_id, self._chain_id, self._node)

    def get_prev_block(self, offset=1):
        return Block(f'{self._block_id}~{offset}', self._chain_id, self._node)

    def get_next_block(self, offset=1):
        return Block(f'{self._block_id}+{offset}', self._chain_id, self._node)
