from os.path import basename, dirname, join

from pytezos.michelson.contract import Contract, micheline_to_michelson
from pytezos.operation.group import OperationGroup
from pytezos.operation.content import format_mutez
from pytezos.interop import Interop


class ContractCall(Interop):

    def __init__(self, parameters, address, amount=0, shell=None, key=None):
        super(ContractCall, self).__init__(shell=shell, key=key)
        self.parameters = parameters
        self.address = address
        self.amount = amount

    def _spawn(self, **kwargs):
        return ContractCall(
            parameters=self.parameters,
            address=self.address,
            amount=kwargs.get('amount', self.amount),
            shell=kwargs.get('shell', self.shell),
            key=kwargs.get('key', self.key)
        )

    def __repr__(self):
        return str(self.operation_group())

    def with_amount(self, amount):
        return self._spawn(amount=amount)

    def operation_group(self) -> OperationGroup:
        return OperationGroup(shell=self.shell, key=self.key) \
            .transaction(destination=self.address,
                         amount=self.amount,
                         parameters=self.parameters) \
            .fill()

    def inject(self):
        return self.operation_group().autofill().sign().inject()

    def cmdline(self):
        arg = micheline_to_michelson(self.parameters, inline=True)
        source = self.key.public_key_hash()
        amount = format_mutez(self.amount)
        return f'transfer {amount} from {source} to {self.address} -arg "{arg}"'


class ContractEntrypoint(Interop):

    def __init__(self, name, address, contract: Contract = None, shell=None, key=None):
        super(ContractEntrypoint, self).__init__(shell=shell, key=key)
        if contract is None:
            code = self.shell.contracts[address].script().get('code')
            contract = Contract.from_micheline(code)

        self.contract = contract
        self.name = name
        self.address = address

    def _spawn(self, **kwargs):
        return ContractEntrypoint(
            name=self.name,
            contract=self.contract,
            address=self.address,
            shell=kwargs.get('shell', self.shell),
            key=kwargs.get('key', self.key),
        )

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

        parameters = self.contract.parameter.encode(data)
        return ContractCall(
            parameters=parameters,
            address=self.address,
            shell=self.shell,
            key=self.key,
        )


class ContractInterface(Interop):
    default_entry = 'call'

    def __init__(self, address, contract: Contract = None, shell=None, key=None):
        super(ContractInterface, self).__init__(shell=shell, key=key)
        if contract is None:
            code = self.shell.contracts[address].script().get('code')
            contract = Contract.from_micheline(code)

        self.contract = contract
        self.address = address

        for entry_name, docstring in contract.parameter.entries(default=self.default_entry):
            entry_point = ContractEntrypoint(
                name=entry_name if entry_name != self.default_entry else None,
                address=self.address,
                contract=contract,
                shell=self.shell,
                key=self.key
            )
            entry_point.__doc__ = docstring
            setattr(self, entry_name, entry_point)

    def _spawn(self, **kwargs):
        return ContractInterface(
            address=self.address,
            contract=self.contract,
            shell=kwargs.get('shell', self.shell),
            key=kwargs.get('key', self.key)
        )

    def __repr__(self):
        return str(self.contract.parameter)

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
