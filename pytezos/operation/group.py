from pprint import pformat

from pytezos.rpc import RpcError
from pytezos.crypto import blake2b_32
from pytezos.operation.content import ContentMixin
from pytezos.operation.forge import forge_operation_group
from pytezos.operation.fees import FeesProvider
from pytezos.encoding import forge_base58, base58_encode
from pytezos.interop import Interop
from pytezos.tools.docstring import get_class_docstring

validation_passes = {
    'endorsement': 0,
    'proposal': 1,
    'ballot': 1,
    'seed_nonce_revelation': 2,
    'double_endorsement_evidence': 2,
    'double_baking_evidence': 2,
    'activate_account': 2,
    'reveal': 3,
    'transaction': 3,
    'origination': 3,
    'delegation': 3
}


class OperationGroup(Interop, ContentMixin):

    def __init__(self, contents=None, protocol=None, branch=None, signature=None, shell=None, key=None):
        super(OperationGroup, self).__init__(shell=shell, key=key)
        self.contents = contents or []
        self.protocol = protocol
        self.branch = branch
        self.signature = signature

    def __repr__(self):
        res = [
            super(OperationGroup, self).__repr__(),
            '\nPayload',
            pformat(self.json_payload()),
            '\nHelpers',
            get_class_docstring(self.__class__)
        ]
        return '\n'.join(res)

    def _spawn(self, **kwargs):
        return OperationGroup(
            contents=kwargs.get('contents', self.contents.copy()),
            protocol=kwargs.get('protocol', self.protocol),
            branch=kwargs.get('branch', self.branch),
            signature=kwargs.get('signature', self.signature),
            shell=kwargs.get('shell', self.shell),
            key=kwargs.get('key', self.key)
        )

    def json_payload(self) -> dict:
        """
        Get json payload used for preapply.
        :return: dic
        """
        return {
            'protocol': self.protocol,
            'branch': self.branch,
            'contents': self.contents,
            'signature': self.signature
        }

    def binary_payload(self) -> bytes:
        """
        Get binary payload used for injection/hash calculation.
        :return: bytes
        """
        if not self.signature:
            raise ValueError('Not signed')

        return bytes.fromhex(self.forge()) + forge_base58(self.signature)

    def operation(self, content):
        """
        Create new operation group with extra content added.
        :param content: Kind-specific operation body
        :return: OperationGroup
        """
        return self._spawn(contents=self.contents + [content])

    def fill(self):
        """
        Try to fill all fields left unfilled, use approximate fees
        (not optimal, use `autofill` to simulate operation and get precise values).
        :return: OperationGroup
        """
        branch = self.branch or self.shell.head.predecessor.hash()
        protocol = self.protocol or self.shell.head.header()['protocol']
        source = self.key.public_key_hash()
        counter = self.shell.contracts[source].count()
        fees_provider = FeesProvider.from_protocol(protocol)

        replace_map = {
            'pkh': source,
            'source': source,
            'delegate': source,
            'counter': lambda x: str(next(counter)),
            'secret': lambda x: self.key.activation_code,
            'period': lambda x: str(self.shell.head.voting_period()),
            'public_key': lambda x: self.key.public_key(),
            'manager_pubkey': source,  # I know, it hurts
            'fee': lambda x: str(fees_provider.fee(x)),
            'gas_limit': lambda x: str(fees_provider.gas_limit(x)),
            'storage_limit': lambda x: str(fees_provider.storage_limit(x)),
        }

        def fill_content(content):
            content = content.copy()
            for k, v in replace_map.items():
                if content.get(k) in ['', '0']:
                    content[k] = v(content) if callable(v) else v
            return content

        return self._spawn(
            contents=list(map(fill_content, self.contents)),
            protocol=protocol,
            branch=branch
        )

    def run(self):
        """
        Simulate operation without signature checks.
        :return: RPC response
        """
        return self.shell.head.helpers.scripts.run_operation.post({
            'branch': self.branch,
            'contents': self.contents,
            'signature': base58_encode(b'0' * 64, b'sig').decode()
        })

    def forge(self, validate=True):
        """
        Convert json representation of the operation group into bytes
        :param validate: Forge remotely also and compare results, default is True
        :return: Hex string
        """
        payload = {
            'branch': self.branch,
            'contents': self.contents
        }
        local_data = forge_operation_group(payload).hex()

        if validate:
            remote_data = self.shell.blocks[self.branch].helpers.forge.operations.post(payload)
            if local_data != remote_data:
                raise ValueError(f'Local forge result differs from remote one:\n\n{local_data}\n\n{remote_data}')

        return local_data

    def autofill(self):
        """
        Fill the gaps and then simulate the operation in order to calculate fee, gas/storage limits.
        :return: OperationGroup
        """
        opg = self.fill()
        opg_with_metadata = opg.run()
        fees_provider = FeesProvider.from_protocol(opg.protocol)
        extra_size = (32 + 64) // len(opg.contents) + 1  # size of serialized branch and signature)

        def res_limits(res):
            if res['status'] != 'applied':
                raise ValueError(f'Operation has failed\n\n{res}')
            return int(res.get('consumed_gas', 0)), int(res.get('paid_storage_size_diff', 0))

        def fill_content(content):
            operation_result = content['metadata'].get('operation_result')
            if operation_result:
                internal_operation_result = content['metadata'].get('internal_operation_result', [])

                consumed = [res_limits(operation_result)] + list(map(res_limits, internal_operation_result))
                consumed_gas, paid_storage_diff = tuple(map(sum, zip(*consumed)))
                fee = fees_provider.calculate_fee(content, consumed_gas, extra_size)

                content.update(
                    gas_limit=str(consumed_gas),
                    storage_limit=str(paid_storage_diff + fees_provider.burn_cap(content)),
                    fee=str(fee)
                )

            content.pop('metadata')
            return content

        opg.contents = list(map(fill_content, opg_with_metadata['contents']))
        return opg

    def sign(self):
        """
        Sign the operation group with the key specified by `using`.
        :return: OperationGroup
        """
        validation_pass = validation_passes[self.contents[0]['kind']]
        if any(map(lambda x: validation_passes[x['kind']] != validation_pass, self.contents)):
            raise ValueError('Mixed validation passes')

        if validation_pass == 0:
            chain_watermark = bytes.fromhex(self.shell.chains.main.watermark())
            watermark = b'\x02' + chain_watermark
        else:
            watermark = b'\x03'

        message = watermark + bytes.fromhex(self.forge())
        signature = self.key.sign(message=message, generic=True)

        return self._spawn(signature=signature)

    def hash(self):
        """
        Calculate the Base58 encoded operation group hash.
        :return: str
        """
        hash_digest = blake2b_32(self.binary_payload()).digest()
        return base58_encode(hash_digest, b'o').decode()

    def preapply(self):
        """
        Preapply signed operation group.
        :return: RPC response
        """
        if not self.signature:
            raise ValueError('Not signed')

        return self.shell.head.helpers.preapply.operations.post(
            operations=[self.json_payload()])

    def inject(self, _async=False):
        """
        Inject signed operation group.
        :param _async: default is False
        :return: RPC response (operation group hash)
        """
        try:
            self.preapply()
        except RpcError as e:
            return e.res.text

        return self.shell.injection.operation.post(
            operation=self.binary_payload(), _async=_async)
