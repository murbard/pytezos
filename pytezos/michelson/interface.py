from os.path import basename, dirname, join

from pytezos.rpc import ShellQuery
from pytezos.crypto import Key
from pytezos.michelson.contract import Contract, ContractParameter, micheline_to_michelson
from pytezos.operation.group import OperationGroup
from pytezos.operation.content import format_mutez


class ContractInterop:

    def __init__(self, shell: ShellQuery, key: Key, address):
        self.shell = shell
        self.key = key
        self.address = address


class ContractCall(ContractInterop):

    def __init__(self, parameters, amount=0, **kwargs):
        super(ContractCall, self).__init__(**kwargs)
        self.parameters = parameters
        self.amount = amount

    def __repr__(self):
        return str(self.operation_group())

    def with_amount(self, amount):
        return ContractCall(
            self.parameters,
            amount,
            shell=self.shell,
            key=self.key,
            address=self.address
        )

    def operation_group(self) -> OperationGroup:
        return OperationGroup(shell=self.shell, key=self.key) \
            .transaction(destination=self.address, amount=self.amount, parameters=self.parameters) \
            .fill()

    def inject(self):
        return self.operation_group().autofill().sign().inject()

    def cmdline(self):
        arg = micheline_to_michelson(self.parameters, inline=True)
        source = self.key.public_key_hash()
        amount = format_mutez(self.amount)
        return f'transfer {amount} from {source} to {self.address} -arg "{arg}"'


class ContractEntrypoint(ContractInterop):

    def __init__(self, name, parameter: ContractParameter, **kwargs):
        super(ContractEntrypoint, self).__init__(**kwargs)
        self.name = name
        self.parameter = parameter

    def __repr__(self):
        return self.__doc__

    def __call__(self, *args, **kwargs):
        if args:
            if len(args) == 1:
                data = args[0]
            else:
                data = list(args)
        elif kwargs:
            data = kwargs
        else:
            data = []

        if self.name:
            data = {self.name: data} if data else self.name

        parameters = self.parameter.encode(data)
        return ContractCall(
            parameters,
            shell=self.shell,
            key=self.key,
            address=self.address
        )


class ContractInterface(ContractInterop):
    default_entry = 'call'

    def __init__(self, contract: Contract, **kwargs):
        super(ContractInterface, self).__init__(**kwargs)
        self.contract = contract
        for entry_name, docstring in contract.parameter.entries(default=self.default_entry):
            entry_point = ContractEntrypoint(
                entry_name if entry_name != self.default_entry else None,
                contract.parameter,
                shell=self.shell,
                key=self.key,
                address=self.address
            )
            entry_point.__doc__ = docstring
            setattr(self, entry_name, entry_point)

    def __repr__(self):
        return str(self.contract.parameter)

    @classmethod
    def from_address(cls, shell, key, address):
        code = shell.contracts[address].script().get('code')
        contract = Contract.from_micheline(code)
        return ContractInterface(
            contract,
            shell=shell,
            key=key,
            address=address
        )

    def big_map_get(self, path, block_id='head'):
        key = basename(path)
        big_map_path = dirname(path)
        big_map_path = join('/', big_map_path) if big_map_path else None
        query = self.contract.storage.big_map_query(key, big_map_path)
        value = self.shell.blocks[block_id].context.contracts[self.address].big_map_get.post(query)
        return self.contract.storage.big_map_decode(value, big_map_path)

    def storage(self, block_id='head'):
        storage = self.shell.blocks[block_id].context.contracts[self.address].storage()
        return self.contract.storage.decode_storage(storage)
