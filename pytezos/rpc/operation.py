from binascii import hexlify
from functools import lru_cache

from pytezos.crypto import Key, blake2b_32
from pytezos.encoding import base58_decode, base58_encode
from pytezos.rpc.node import RpcQuery


class OperationListList(RpcQuery):

    def __iter__(self):
        operations = super(OperationListList, self).__call__()
        for operation_group in operations:
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


class Operation(RpcQuery):

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

    def unsigned(self) -> dict:
        operation = self()
        return {
            'branch': operation['branch'],
            'contents': [
                {k: v for k, v in c.items() if k != 'metadata'}
                for c in operation['contents']
            ]
        }

    def forge(self):
        return self._node.post(
            path='chains/main/blocks/head/helpers/forge/operations',
            json=self.unsigned(),
            cache=True
        )

    def unsigned_raw(self):
        return '03' + self.forge()

    def sign(self, key):
        if isinstance(key, str):
            key = Key(key)
        if not isinstance(key, Key):
            raise ValueError('Base58 encoded secret key or Key instance required.')

        self._data['signature'] = key.sign(self.unsigned_raw(), generic=True)
        return self._data['signature']

    def raw(self):
        signature_raw = base58_decode(self.get('signature').encode())
        return self.forge() + hexlify(signature_raw).decode()

    def signed(self) -> dict:
        return {
            'protocol': self.get('protocol', 'PsddFKi32cMJ2qPjf43Qv5GDWLDPZb3T3bF6fLKiF5HtvHNU7aP'),
            'signature': self.get('signature'),
            **self.unsigned()
        }

    def preapply(self, branch=None) -> dict:
        operation = self.signed()
        if branch is None:
            branch = operation['branch']

        res = self._node.post(
            path=f'chains/main/blocks/{branch}/helpers/preapply/operations',
            json=[operation],
            cache=True
        )
        self._data['contents'] = res[0]['contents']
        return res[0]

    def hash(self):
        hash_digest = blake2b_32(self.raw()).digest()
        return base58_encode(hash_digest, b'o').decode()

    def signer_pkh(self):
        content = self.get('contents')[0]
        if content['kind'] == 'endorsement':
            return content['metadata']['delegate']
        if content['kind'] == 'transaction':
            return content['source']
        raise NotImplementedError
