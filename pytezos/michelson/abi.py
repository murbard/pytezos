from pytezos.rpc import ShellQuery
from pytezos.crypto import Key
from pytezos.michelson.contract import Contract
from pytezos.operation.group import OperationGroup


class ContractInterop:

    def __init__(self, shell: ShellQuery, key: Key, address, contract: Contract):
        self.shell = shell
        self.key = key
        self.address = address
        self.contract = contract


class ContractEntry(ContractInterop):

    def call(self, *args, **kwargs):
        if args:
            assert len(kwargs) == 0
            if len(args) == 1:
                data = args[0]
            else:
                data = list(args)
            parameters = self.contract.michel_to_micheline(data, 'parameter')
        elif kwargs:
            assert len(args) == 0
            parameters = self.contract.michel_to_micheline(kwargs, 'parameter')
        else:
            parameters = []

        return OperationGroup(shell=self.shell, key=self.key) \
            .transaction(destination=self.address, parameters=parameters) \
            .autofill() \
            .sign()


class ContractEntries(ContractInterop):

    def __getitem__(self, item) -> ContractEntry:
        pass


class ContractAbi(ContractInterop):

    @classmethod
    def from_address(cls, shell, key, address):
        contract = Contract.from_micheline(shell.contracts[address].script().get('code'))
        abi = cls(shell=shell, key=key, address=address, contract=contract)



    def big_map_get(self, key):
        pass

    def storage(self, block_id='head'):
        storage = self.shell.blocks[block_id].context.contracts[self.address].storage()
        return self.contract.micheline_to_michel(storage, 'storage')

    # @property
    # def entries(self) -> ContractEntries:
    #     return ContractEntries(
    #         shell=self.shell,
    #         key=self.key,
    #         address=self.address,
    #         contract=self.contract
    #     )
    #
    # def __repr__(self):
    #     return ''
    #
    # def __dir__(self):
    #     return list(super(ContractClass, self).__dir__()) + list(self.entries.__dir__())
    #
    # def __getattr__(self, item) -> ContractEntry:
    #     return self.entries[item]
