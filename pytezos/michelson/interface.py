from os.path import basename, dirname, join
from pprint import pformat

from pytezos.michelson.contract import Contract, micheline_to_michelson
from pytezos.operation.group import OperationGroup
from pytezos.operation.content import format_mutez
from pytezos.interop import Interop
from pytezos.tools.docstring import get_class_docstring


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
        res = [
            super(ContractCall, self).__repr__(),
            '\nPayload',
            pformat(self.operation_group.json_payload()),
            '\nHelpers',
            get_class_docstring(self.__class__)
        ]
        return '\n'.join(res)

    def with_amount(self, amount):
        """
        Send funds to the contract too.
        :param amount: amount in microtez (int) or tez (Decimal)
        :return: ContractCall
        """
        return self._spawn(amount=amount)

    @property
    def operation_group(self) -> OperationGroup:
        """
        Show generated operation group.
        :return: OperationGroup
        """
        return OperationGroup(shell=self.shell, key=self.key) \
            .transaction(destination=self.address,
                         amount=self.amount,
                         parameters=self.parameters) \
            .fill()

    def inject(self):
        """
        Autofill, sign and inject resulting operation group.
        :return: RPC response (operation group hash)
        """
        return self.operation_group.autofill().sign().inject()

    def cmdline(self):
        """
        Generate command line for tezos client.
        :return: str
        """
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
        res = [
            super(ContractEntrypoint, self).__repr__(),
            f'.address -> {self.address}',
            f'\n{self.__doc__}'
        ]
        return '\n'.join(res)

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
    __default_entry__ = 'call'

    def __init__(self, address, contract: Contract = None, shell=None, key=None):
        super(ContractInterface, self).__init__(shell=shell, key=key)
        if contract is None:
            code = self.shell.contracts[address].script().get('code')
            contract = Contract.from_micheline(code)

        self.contract = contract
        self.address = address

        for entry_name, docstring in contract.parameter.entries(default=self.__default_entry__):
            entry_point = ContractEntrypoint(
                name=entry_name if entry_name != self.__default_entry__ else None,
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
        entrypoints, _ = zip(*self.contract.parameter.entries(default=self.__default_entry__))
        res = [
            super(ContractInterface, self).__repr__(),
            f'.address -> {self.address}',
            '\nEntrypoints',
            *list(map(lambda x: f'.{x}()', entrypoints)),
            '\nHelpers',
            get_class_docstring(self.__class__,
                                attr_filter=lambda x: not x.startswith('_') and x not in entrypoints)
        ]
        return '\n'.join(res)

    def big_map_get(self, path, block_id='head'):
        """
        Get BigMap entry as Python object by plain key and block height
        :param path: Json path to the key (or just key to access default BigMap location)
        :param block_id: Block height / hash / offset to use, default is `head`
        :return: object
        """
        key = basename(path)
        big_map_path = dirname(path)
        big_map_path = join('/', big_map_path) if big_map_path else None
        query = self.contract.storage.big_map_query(key, big_map_path)
        value = self.shell.blocks[block_id].context.contracts[self.address].big_map_get.post(query)
        return self.contract.storage.big_map_decode(value, big_map_path)

    def storage(self, block_id='head'):
        """
        Get storage as Pythons object at specified block height.
        :param block_id: Block height / hash / offset to use, default is `head`
        :return: object
        """
        storage = self.shell.blocks[block_id].context.contracts[self.address].storage()
        return self.contract.storage.decode(storage)
