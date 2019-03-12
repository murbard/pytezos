from datetime import datetime
from functools import lru_cache
from pendulum.parsing.exceptions import ParserError
import pendulum
import os

from pytezos.rpc.context import Context
from pytezos.rpc.node import RpcQuery, urljoin
from pytezos.rpc.operation import Operation, OperationListList
from pytezos.rpc.votes import Votes
from pytezos.rpc.helpers import HelpersMixin
from pytezos.crypto import blake2b_32, Key
from pytezos.encoding import base58_encode, is_bh


def to_timestamp(v):
    try:
        v = pendulum.parse(v)
    except ParserError:
        pass
    if isinstance(v, datetime):
        v = int(v.timestamp())
    return v


class BlockListList(RpcQuery):

    def __call__(self, length=1, head=None, min_date=None):
        if isinstance(head, str) and not is_bh(head):
            head = self.__getitem__(head).calculate_hash()

        if min_date and not isinstance(min_date, int):
            min_date = to_timestamp(min_date)

        return super(BlockListList, self).__call__(length=length, head=head, min_date=min_date)

    def __getitem__(self, item):
        if isinstance(item, slice):
            if not isinstance(item.start, int):
                raise NotImplementedError('Slice start should be an integer.')

            if item.stop is None:
                block_id = 'head'
            elif isinstance(item.stop, int):
                if item.stop < 0:
                    block_id = f'head~{abs(item.stop)}'
                else:
                    block_id = item.stop
            else:
                raise NotImplementedError('Slice stop can be an integer or None.')

            header = self.__getitem__(block_id).header()

            if item.start < 0:
                length = abs(item.start)
                if isinstance(item.stop, int) and item.stop < 0:
                    length -= abs(item.stop)
            else:
                length = header['level'] - item.start

            return self.__call__(length=length, head=header['hash'])

        return super(BlockListList, self).__getitem__(item)


class BlockHeader(RpcQuery, HelpersMixin):

    def __init__(self, *args, **kwargs):
        super(BlockHeader, self).__init__(
            properties=['shell', 'protocol_data', 'raw'],
            *args, **kwargs)

    def watermark(self):
        return '01' + self.get_chain_watermark()

    def unsigned_data(self):
        data = self.shell()
        data['protocol_data'] = self.protocol_data.signed_bytes()[:-128]
        return data

    def unsigned_bytes(self):
        return self.watermark() + self.forge()

    def calculate_hash(self):
        hash_digest = blake2b_32(self.raw()).digest()
        return base58_encode(hash_digest, b'B').decode()

    def calculate_pow_stamp(self):
        hash_digest = blake2b_32(self.forge() + '0' * 128).digest()
        return int.from_bytes(hash_digest, byteorder='big')

    def forge(self):
        data = self._node.post(
            path='chains/main/blocks/head/helpers/forge_block_header',
            json=self.unsigned_data()
        )
        return data['block']


class Block(RpcQuery, HelpersMixin):

    def __init__(self, *args, **kwargs):
        kwargs.update(
            cache='head' not in kwargs.get('path', ''),
            block_id=os.path.basename(kwargs.get('path', ''))
        )
        super(Block, self).__init__(
            properties={
                'hash': RpcQuery,
                'header': BlockHeader,
                'context': Context,
                'metadata': RpcQuery
            },
            *args, **kwargs)

    @property
    @lru_cache(maxsize=None)
    def operations(self):
        return OperationListList(
            path=f'{self._path}/operations',
            node=self._node,
            child_class=Operation,
            **self._kwargs
        )

    @property
    @lru_cache(maxsize=None)
    def operation_hashes(self):
        return OperationListList(
            path=f'{self._path}/operation_hashes',
            node=self._node,
            child_class=RpcQuery,
            **self._kwargs
        )

    @property
    def votes(self):
        return Votes(
            path=f'{self._path}/votes',
            node=self._node,
            **self._kwargs
        )

    def freeze(self):
        """
        Returns fixed-hash block, useful for aliases, like head, head~1, etc.
        :return: Block instance with hash initialized
        """
        return Block(
            path=urljoin(os.path.dirname(self._path), self.hash()),
            node=self._node,
            **self._kwargs
        )

    @property
    def predecessor(self):
        return Block(
            path=urljoin(os.path.dirname(self._path), self.header.get('predecessor')),
            node=self._node,
            **self._kwargs
        )

    def level(self) -> int:
        return self.metadata.get('level')['level']

    def cycle(self) -> int:
        return self.metadata.get('level')['cycle']

    def create_endorsement(self) -> Operation:
        header = self.header()
        return Operation(data={
            'branch': header['hash'],
            'contents': [{
                'kind': 'endorsement',
                'level': header['level']
            }]
        })

    def verify_signature(self):
        pk = self.get_public_key(self.metadata.get('baker'))
        Key(pk).verify(self.header.get('signature'), self.header.unsigned_bytes())
