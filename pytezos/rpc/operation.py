from binascii import hexlify
from functools import lru_cache

from pytezos.crypto import Key, blake2b_32
from pytezos.encoding import base58_decode, base58_encode
from pytezos.rpc.node import RpcQuery
from pytezos.rpc.helpers import HelpersMixin


def get_pass_by_kind(kind) -> int:
    if kind == 'endorsement':
        return 0
    if kind in {'proposals', 'ballot'}:
        return 1
    if kind in {'seed_nonce_revelation', 'double_endorsement_evidence',
                'double_baking_evidence', 'activate_account'}:
        return 2
    if kind in {'reveal', 'transaction', 'origination', 'delegation'}:
        return 3
    raise NotImplementedError(kind)


def filter_operations(operations, kind=None, recursive=True):
    if isinstance(kind, str):
        kind = {kind}
    elif isinstance(kind, list):
        kind = set(kind)

    def multiple_content(op):
        # manager operations can be spawned by a smart contract
        return any(map(lambda ct: ct['kind'] in kind, op['contents']))

    def single_content(op):
        return op['contents'][0]['kind'] in kind

    if get_pass_by_kind(kind) == 3 and recursive:
        f = multiple_content
    else:
        f = single_content

    return filter(f, operations)


class OperationListList(RpcQuery):

    def __iter__(self):
        for operation_group in self():
            for operation in operation_group:
                yield operation

    def __call__(self, kind=None, recursive_search=True):
        """
        :param kind: endorsement, seed_nonce_revelation, double_endorsement_evidence, double_baking_evidence,
        activate_account, proposals, ballot, reveal, transaction, origination, delegation
        :return: flat list of operations filtered by kind (recursive search)
        """
        if kind:
            validation_pass = get_pass_by_kind(kind)
            return list(filter_operations(
                operations=self[validation_pass](),
                kind=kind,
                recursive=recursive_search
            ))
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

    @property
    def endorsements(self):
        """
        The first list contains the endorsements (kind `endorsement`)
        :return: RPCQuery instance
        """
        return self[0]

    @property
    def votes(self):
        """
        The second list contains all the operations regarding votes and proposals (kind `proposals`, `ballot`)
        :return: RPCQuery instance
        """
        return self[1]

    @property
    def anonymous(self):
        """
        The third list contains anonymous operations (kind `seed_nonce_revelation`, `double_endorsement_evidence`,
            `double_baking_evidence`, `activate_account`)
        :return: RPCQuery instance
        """
        return self[2]

    @property
    def managers(self):
        """
        The last one contains the manager operations (`reveal`, `transaction`, `origination`, `delegation`)
        :return: RPCQuery instance
        """
        return self[3]


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

    @classmethod
    def from_data(cls, data: dict):
        return Operation(data)

    def watermark(self):
        content = self.get('contents')[0]
        kind = content['kind']
        if kind in ['endorsement', 'seed_nonce_revelation']:
            return '02' + self.get_chain_watermark()
        if kind in ['transaction', 'origination', 'delegation', 'reveal', 'ballot', 'proposals', 'activate_account']:
            return '03'
        raise NotImplementedError(kind)

    def source(self):
        content = self.get('contents')[0]
        kind = content['kind']
        if kind in ['endorsement']:
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
        signature_bytes = hexlify(base58_decode(self.get('signature'))).decode()
        return self.forge() + signature_bytes

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
        pk = self.get_public_key(self.source())
        Key(pk).verify(self.get('signature'), self.unsigned_bytes())
