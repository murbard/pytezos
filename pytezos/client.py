from functools import lru_cache

from pytezos.operation.group import OperationGroup
from pytezos.operation.content import ContentMixin
from pytezos.michelson.interface import ContractInterface
from pytezos.interop import Interop
from pytezos.tools.docstring import get_class_docstring


class PyTezosClient(Interop, ContentMixin):

    def __repr__(self):
        res = [
            super(PyTezosClient, self).__repr__(),
            '\nHelpers',
            get_class_docstring(self.__class__)
        ]
        return '\n'.join(res)

    def _spawn(self, **kwargs):
        return PyTezosClient(
            shell=kwargs.get('shell', self.shell),
            key=kwargs.get('key', self.key)
        )

    def operation_group(self, protocol=None, branch=None, contents=None, signature=None) -> OperationGroup:
        """
        Create new operation group (multiple contents).
        You can leave all fields empty in order to create an empty operation group.
        :param protocol: Leave None for autocomplete, otherwise you know what to do
        :param branch: Leave None for autocomplete
        :param contents: List of operation contents (optional)
        :param signature: Can be set later
        :return: OperationGroup
        """
        return OperationGroup(
            protocol=protocol,
            branch=branch,
            contents=contents,
            signature=signature,
            shell=self.shell,
            key=self.key
        )

    def operation(self, content: dict) -> OperationGroup:
        """
        Create an operation group with single content
        :param content: Operation body (depending on `kind`)
        :return: OperationGroup
        """
        return OperationGroup(
            contents=[content],
            shell=self.shell,
            key=self.key
        )

    def account(self, account_id=None) -> dict:
        """
        Shortcut for RPC contract request
        :param account_id: tz/KT address, leave None to show info about current key
        :return: dict
        """
        address = account_id or self.key.public_key_hash()
        return self.shell.contracts[address]()

    @lru_cache(maxsize=None)
    def _get_contract_interface(self, contract_id):
        return ContractInterface(
            address=contract_id,
            shell=self.shell,
            key=self.key
        )

    def contract(self, contract_id) -> ContractInterface:
        """
        Get a high-level interface for a given smart contract id.
        :param contract_id: KT address of a smart contract
        :return: ContractInterface
        """
        return self._get_contract_interface(contract_id)
