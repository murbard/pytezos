from pprint import pformat

from pytezos.rpc import ShellQuery, RpcError
from pytezos.crypto import Key
from pytezos.operation.content import ContentMixin
from pytezos.operation.forge import forge_operation_group
from pytezos.operation.fees import FeesProvider
from pytezos.encoding import forge_base58, base58_encode

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


class OperationGroup(ContentMixin):

    def __init__(self, shell: ShellQuery, key: Key, contents=None, protocol=None, branch=None, signature=None):
        self.shell = shell
        self.key = key
        self.contents = contents or []
        self.protocol = protocol
        self.branch = branch
        self.signature = signature

    def __repr__(self):
        return pformat(self.payload())

    @property
    def validation_pass(self):
        return validation_passes[self.contents[0]['kind']] if self.contents else None

    def payload(self):
        return {
            'protocol': self.protocol,
            'branch': self.branch,
            'contents': self.contents,
            'signature': self.signature
        }

    def operation(self, content):
        if self.contents and validation_passes[content['kind']] != self.validation_pass:
            raise ValueError('Mixed validation passes')

        return OperationGroup(
            shell=self.shell,
            key=self.key,
            contents=self.contents + [content],
            branch=self.branch,
            protocol=self.protocol
        )

    def fill(self):
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
            'manager_pubkey': lambda x: self.key.public_key(),
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

        return OperationGroup(
            shell=self.shell,
            key=self.key,
            contents=list(map(fill_content, self.contents)),
            protocol=protocol,
            branch=branch
        )

    def run(self):
        return self.shell.head.helpers.scripts.run_operation.post({
            'branch': self.branch,
            'contents': self.contents,
            'signature': base58_encode(b'0' * 64, b'sig').decode()
        })

    def forge(self, validate=True):
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
        opg = self.fill()
        opg_with_metadata = opg.run()
        fees_provider = FeesProvider.from_protocol(opg.protocol)
        extra_size = (32 + 64) // len(opg.contents) + 1  # size of serialized branch and signature)

        def res_limits(res):
            if res['status'] != 'applied':
                raise ValueError(f'Operation has failed\n\n{res}')
            return int(res.get('consumed_gas', 0)), int(res.get('paid_storage_size_diff', 0))

        def fill_content(content):
            consumed = [res_limits(content['metadata']['operation_result'])] \
                + list(map(res_limits, content['metadata'].get('internal_operation_result', [])))

            consumed_gas, paid_storage_diff = tuple(map(sum, zip(*consumed)))
            fee = fees_provider.calculate_fee(content, consumed_gas, extra_size)

            content.update(
                gas_limit=str(consumed_gas),
                storage_limit=str(paid_storage_diff),
                fee=str(fee)
            )
            content.pop('metadata')
            return content

        opg.contents = list(map(fill_content, opg_with_metadata['contents']))
        return opg

    def sign(self):
        if self.validation_pass == 0:
            chain_watermark = bytes.fromhex(self.shell.chains.main.watermark())
            watermark = b'\x02' + chain_watermark
        else:
            watermark = b'\x03'

        message = watermark + bytes.fromhex(self.forge())
        signature = self.key.sign(message=message, generic=True)

        return OperationGroup(
            shell=self.shell,
            key=self.key,
            contents=self.contents,
            signature=signature,
            branch=self.branch,
            protocol=self.protocol
        )

    def preapply(self):
        if not self.signature:
            raise ValueError('Not signed')

        return self.shell.head.helpers.preapply.operations.post([self.payload()])

    def inject(self, _async=False):
        if not self.signature:
            raise ValueError('Not signed')

        try:
            self.preapply()
        except RpcError as e:
            return e.res.text

        data = bytes.fromhex(self.forge()) + forge_base58(self.signature)
        return self.shell.injection.operation.post(data, _async=_async)
