from binascii import hexlify
from functools import lru_cache

from pytezos.crypto import Key, blake2b_32
from pytezos.encoding import base58_decode, base58_encode
from pytezos.rpc.node import RpcQuery
from pytezos.rpc.helpers import HelpersMixin


class OperationListList(RpcQuery):

    def __iter__(self):
        for operation_group in self():
            for operation in operation_group:
                yield operation

    def __call__(self, kind=None):
        """
        :param kind: endorsement, seed_nonce_revelation, double_endorsement_evidence, double_baking_evidence,
        activate_account, proposals, ballot, reveal, transaction, origination, delegation
        :return: flat list of operations filtered by kind
        """
        if kind:
            return list(filter(lambda x: x['contents'][0]['kind'] == kind, iter(self)))
        return super(OperationListList, self).__call__()

    @lru_cache(maxsize=None)
    def __getitem__(self, item):
        if isinstance(item, tuple):
            return self._child_class(
                path=f'{self._path}/{item[0]}/{item[1]}',
                node=self._node,
                cache=self._cache
            )
        elif isinstance(item, int):
            return RpcQuery(
                path=f'{self._path}/{item}',
                node=self._node,
                cache=self._cache,
                child_class=self._child_class
            )
        else:
            raise NotImplementedError(item)

    def flat(self):
        return list(iter(self))


class Operation(RpcQuery, HelpersMixin):

    def __init__(self, data=None, *args, **kwargs):
        super(Operation, self).__init__(*args, **kwargs)
        self._data = data if data else dict()

    def __repr__(self):
        if self._data:
            return str(self._data)
        return super(Operation, self).__repr__()

    def __call__(self, *args, **kwargs):
        if self._data:
            return self._data
        return super(Operation, self).__call__(*args, **kwargs)

    def watermark(self):
        content = self.get('contents')[0]
        kind = content['kind']
        if kind == ['endorsement', 'seed_nonce_revelation']:
            return '02' + self.get_chain_watermark()
        if kind in ['transaction', 'origination', 'delegation', 'reveal', 'ballot', 'proposals', 'activate_account']:
            return '03'
        raise NotImplementedError(kind)

    def signer_pkh(self):
        content = self.get('contents')[0]
        kind = content['kind']
        if kind in ['endorsement', 'seed_nonce_revelation']:
            return content['metadata']['delegate']
        if kind == 'activate_account':
            return content['pkh']
        if kind in ['transaction', 'origination', 'delegation', 'reveal', 'ballot', 'proposals']:
            return content['source']
        raise NotImplementedError(f'Operation `{kind}` is anonymous.')

    def protocol(self):
        try:
            protocol = self.get('protocol')
        except KeyError:
            branch = self.get("branch")
            protocol = self._node.get(f'chains/main/blocks/{branch}/header').get('protocol')
        return protocol

    def unsigned_data(self) -> dict:
        operation = self()
        return {
            'branch': operation['branch'],
            'contents': [
                {k: v for k, v in c.items() if k != 'metadata'}
                for c in operation['contents']
            ]
        }

    def signed_data(self) -> dict:
        return {
            'protocol': self.protocol(),
            'signature': self.get('signature'),
            **self.unsigned_data()
        }

    def unsigned_bytes(self):
        return self.watermark() + self.forge()

    def signed_bytes(self):
        signature_raw = base58_decode(self.get('signature'))
        return self.forge() + hexlify(signature_raw).decode()

    def calculate_hash(self):
        hash_digest = blake2b_32(self.signed_bytes()).digest()
        return base58_encode(hash_digest, b'o').decode()

    def forge(self):
        return self._node.post(
            path='chains/main/blocks/head/helpers/forge/operations',
            json=self.unsigned_data(),
            cache=True
        )

    def sign(self, key):
        if isinstance(key, str):
            key = Key(key)
        if not isinstance(key, Key):
            raise ValueError('Base58 encoded secret key or Key instance required.')

        self._data['signature'] = key.sign(self.unsigned_bytes(), generic=True)
        return self._data['signature']

    def preapply(self, branch=None):
        operation = self.signed_data()
        if branch is None:
            branch = operation['branch']

        data = self._node.post(
            path=f'chains/main/blocks/{branch}/helpers/preapply/operations',
            json=[operation],
            cache=True
        )
        self._data['contents'] = data[0]['contents']
        return data

    def verify_signature(self):
        pk = self.get_public_key(self.signer_pkh())
        Key(pk).verify(self.get('signature'), self.unsigned_bytes())
