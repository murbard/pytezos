import os
import json
from functools import lru_cache

from pytezos.rpc import ShellQuery
from pytezos.crypto import Key
from pytezos.operation.group import OperationGroup
from pytezos.operation.content import ContentMixin
from pytezos.michelson.interface import ContractInterface
from pytezos.encoding import is_pkh, is_kt, is_key


def get_address(identity, tezos_client_dir='~/.tezos-client'):
    if is_pkh(identity) or is_kt(identity):
        return identity

    addresses = []
    for filename in ['contracts', 'public_key_hashs']:
        path = os.path.expanduser(os.path.join(tezos_client_dir, filename))
        with open(path) as f:
            data = json.loads(f.read())

        addresses.extend([x['value'] for x in data if x['name'] == identity])

    if len(addresses) > 1:
        raise ValueError(f'More than one address found for {identity}')
    if len(addresses) == 0:
        raise ValueError(f'Not found: {identity}')
    return addresses[0]


class PyTezosClient(ContentMixin):

    def __init__(self, shell=None, key=None):
        self.shell = shell  # type: ShellQuery
        self.key = key  # type: Key

    @staticmethod
    def using(key, shell: ShellQuery):
        if isinstance(key, Key):
            pass
        elif is_key(key):
            key = Key.from_encoded_key(key)
        else:
            key = Key.from_alias(key)

        return PyTezosClient(shell, key)

    def operation_group(self, protocol=None, branch=None, contents=None, signature=None) -> OperationGroup:
        return OperationGroup(
            shell=self.shell,
            key=self.key,
            protocol=protocol,
            branch=branch,
            contents=contents,
            signature=signature
        )

    def operation(self, content: dict) -> OperationGroup:
        return OperationGroup(
            shell=self.shell,
            key=self.key,
            contents=[content]
        )

    def account(self, account_id=None):
        address = get_address(account_id) if account_id else self.key.public_key_hash()
        return self.shell.contracts[address]()

    def activate(self):
        return self.activate_account().autofill().sign()

    def reveal_public_key(self, source=''):
        if source:
            source = get_address(source)
        return self.reveal(source=source).autofill().sign()

    def register_delegate(self):
        return self.delegation().autofill().sign()

    def send(self, destination, amount, source=None):
        return self.transaction(
            source=get_address(source) if source else '',
            destination=get_address(destination),
            amount=amount
        ).autofill().sign()

    def deploy(self, source, storage=None):
        return self.origination()

    @lru_cache(maxsize=None)
    def contract(self, contract_id) -> ContractInterface:
        return ContractInterface.from_address(
            shell=self.shell,
            key=self.key,
            address=get_address(contract_id)
        )
