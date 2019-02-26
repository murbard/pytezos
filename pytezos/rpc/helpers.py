from binascii import hexlify

from pytezos.encoding import base58_decode
from pytezos.rpc.node import RpcQuery


class HelpersMixin:

    def get_chain_id(self, default='main'):
        assert isinstance(self, RpcQuery)
        return self._kwargs.get('chain_id', default)

    def get_block_id(self, default='head'):
        assert isinstance(self, RpcQuery)
        return self._kwargs.get('block_id', default)

    def get_manager_key(self, contract_id):
        assert isinstance(self, RpcQuery)
        return self._node.get(f'chains/{self.get_chain_id()}/blocks/{self.get_block_id()}'
                              f'/context/contracts/{contract_id}/manager_key')

    def get_public_key(self, pkh):
        """
        Public key by the public key hash
        :param pkh: public key hash, base58 encoded, i.e. 'tz1eKkWU5hGtfLUiqNpucHrXymm83z3DG9Sq'
        :return: base58 encoded public key
        """
        if pkh.startswith('KT'):  # it is not pkh, but let's handle this
            pkh = self.get_manager_key(pkh).get('manager')

        pk = self.get_manager_key(pkh).get('key')
        if not pk:
            raise ValueError('Public key is not revealed.')

        return pk

    def get_chain_watermark(self):
        assert isinstance(self, RpcQuery)
        data = self._node.get(f'chains/{self.get_chain_id()}/chain_id')
        return hexlify(base58_decode(data.encode())).decode()

    def get_protocol(self, branch='head'):
        assert isinstance(self, RpcQuery)
        return self._node.get(f'chains/{self.get_chain_id()}/blocks/{self.get_block_id(branch)}'
                              f'/header').get('protocol')

    @staticmethod
    def get_level(cycle: int, index=0) -> int:
        return cycle * 4096 + (index % 4096) + 1
