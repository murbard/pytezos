import os
import json
from functools import lru_cache

from pytezos.operation.group import OperationGroup
from pytezos.operation.content import ContentMixin
from pytezos.michelson.interface import ContractInterface, Contract
from pytezos.encoding import is_pkh, is_kt
from pytezos.interop import Interop


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


class PyTezosClient(Interop, ContentMixin):

    def _spawn(self, **kwargs):
        return PyTezosClient(
            shell=kwargs.get('shell', self.shell),
            key=kwargs.get('key', self.key)
        )

    def operation_group(self, protocol=None, branch=None, contents=None, signature=None) -> OperationGroup:
        return OperationGroup(
            protocol=protocol,
            branch=branch,
            contents=contents,
            signature=signature,
            shell=self.shell,
            key=self.key
        )

    def operation(self, content: dict) -> OperationGroup:
        return OperationGroup(
            contents=[content],
            shell=self.shell,
            key=self.key
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

    def transfer(self, destination, amount, source=None):
        return self.transaction(
            source=get_address(source) if source else '',
            destination=get_address(destination),
            amount=amount
        ).autofill().sign()

    def deploy(self, code, storage=None, balance=0):
        if os.path.isfile(code):
            contract = Contract.from_file(code)
        else:
            contract = Contract.from_michelson(code)

        if storage is None:
            storage = contract.storage.default()

        return self.origination(
            code=contract.code,
            storage=storage,
            balance=balance
        )

    @lru_cache(maxsize=None)
    def contract(self, contract_id) -> ContractInterface:
        return ContractInterface(
            address=get_address(contract_id),
            shell=self.shell,
            key=self.key
        )
