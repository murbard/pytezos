from typing import List
from pprint import pformat
from datetime import datetime

from pytezos.rpc.node import Node
from pytezos.rpc.context import Context


class Block:
    __dyn_attrs__ = ['hash', 'header', 'metadata', 'operations']

    def __init__(self, block_id='head', node=Node()):
        self._block_id = block_id
        self._node = node
        self._block = dict()
        self._synced = False

        # if block_id:  # TODO: hash regexp
        #     self._block['hash'] = block_id

    def _sync_all(self):
        if self._block_id == 'head' or not self._synced:
            self._block = self._node.get(f'/chains/{self._node.chain_id}/blocks/{self._block_id}')
            self._synced = True

    def _sync_item(self, item):
        if self._block_id == 'head' or item not in self._block:
            self._block[item] = self._node.get(f'/chains/{self._node.chain_id}/blocks/{self._block_id}/{item}')

    def to_dict(self) -> dict:
        self._sync_all()
        return self._block

    def __dir__(self):
        return sorted(super(Block, self).__dir__() + self.__dyn_attrs__)

    def __repr__(self):
        return pformat(self.to_dict(), compact=True)

    def __getitem__(self, item):
        if item in self.__dyn_attrs__:
            self._sync_item(item)
        else:
            self._sync_all()
        return self._block[item]

    def __getattr__(self, item):
        if item in self.__dyn_attrs__:
            self._sync_item(item)
            return self._block[item]
        else:
            self._sync_all()
            return getattr(self._block, item)

    @property
    def context(self) -> Context:
        return Context(self._block_id, self._node)

    def get_prev_block(self, offset=1):
        return Block(f'{self._block_id}~{offset}', self._node)

    def get_next_block(self, offset=1):
        return Block(f'{self._block_id}+{offset}', self._node)


class BlockSelector:

    def __init__(self, length=1, head=None, min_date=None, node=Node()):
        self._params = dict(
            length=length,
            head=head,
            min_date=int(min_date.timestamp()) if isinstance(min_date, datetime) else min_date
        )
        self._node = node
        self._blocks = list()
        self._synced = False

    def _sync(self):
        if not self._synced:
            hash_matrix = self._node.get(f'/chains/{self._node.chain_id}/blocks', params=self._params)
            self._blocks = [
                list(map(lambda x: Block(x, self._node), hash_row))
                for hash_row in hash_matrix
            ]
            self._synced = True

    def to_list(self, how='all') -> list:
        self._sync()
        if how == 'all':
            return self._blocks
        if how == 'first':
            return next(iter(self._blocks), [])
        if how == 'heads':
            return [row[0].hash for row in self._blocks if len(row) > 0]
        raise NotImplementedError(how)

    def __repr__(self):
        return pformat(self.to_list(), compact=True)

    def __len__(self):
        return len(self.to_list(how='first'))

    def __iter__(self):
        for block in self.to_list(how='first'):
            yield block

    def __getitem__(self, item):
        return self.to_list(how='first')[item]

    @property
    def heads(self) -> List[str]:
        return self.to_list(how='heads')

    @property
    def head(self) -> str:
        return next(iter(self.heads), None)
