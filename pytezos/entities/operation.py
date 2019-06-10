from binascii import hexlify

from pytezos.crypto import Key, blake2b_32
from pytezos.encoding import base58_decode, base58_encode


class Operation:

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
            key = Key.from_key(key)
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
        Key.from_key(pk).verify(self.get('signature'), self.unsigned_bytes())

    def contents(self, kind=None):
        return filter_contents(self(), kind)
