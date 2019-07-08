from pytezos.crypto import blake2b_32, Key
from pytezos.encoding import base58_encode


class BlockHeader:

    def __init__(self, header):
        self._header = header

    def watermark(self):
        return '01' + self.get_chain_watermark()

    def unsigned_data(self):
        data = self.shell()
        data['protocol_data'] = self.protocol_data.raw()[:-128]
        return data

    def unsigned_bytes(self):
        return self.watermark() + self.forge()

    def calculate_hash(self):
        hash_digest = blake2b_32(self.raw()).digest()
        return base58_encode(hash_digest, b'B').decode()

    def calculate_pow_stamp(self):
        hash_digest = blake2b_32(self.forge() + '0' * 128).digest()
        return int.from_bytes(hash_digest, byteorder='big')


class Block:

    def __init__(self, block):
        self._block = block

    def verify_signature(self):
        pk = self.get_public_key(self.metadata.get('baker'))
        Key.from_key(pk).verify(self.header.get('signature'), self.header.unsigned_bytes())
