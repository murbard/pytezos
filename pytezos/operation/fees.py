from pytezos.operation.forge import forge_operation


class FeesProvider:
    __providers__ = dict()

    @classmethod
    def __init_subclass__(cls, protocol='', **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__providers__[protocol] = cls

    @classmethod
    def from_protocol(cls, protocol):
        return cls.__providers__[protocol]()

    def fee(self, content):
        raise NotImplementedError

    def gas_limit(self, content):
        raise NotImplementedError

    def storage_limit(self, content):
        raise NotImplementedError

    def burn_cap(self, content):
        raise NotImplementedError


class Athens004FeesProvider(FeesProvider, protocol='Pt24m4xiPbLDhVgVfABUjirbmda3yohdN82Sp9FeuAXJ4eV9otd'):
    hard_gas_limit_per_operation = 400000
    hard_storage_limit_per_operation = 60000
    minimal_fees = 100
    minimal_nanotez_per_byte = 1
    minimal_nanotez_per_gas_unit = .1

    def calculate_fee(self, content, consumed_gas, extra_size, reserve=10):
        size = len(forge_operation(content)) + extra_size
        fee = self.minimal_fees \
            + self.minimal_nanotez_per_byte * size \
            + int(self.minimal_nanotez_per_gas_unit * consumed_gas)
        return fee + reserve

    def fee(self, content):
        return self.calculate_fee(
            content=content,
            consumed_gas=self.gas_limit(content),
            extra_size=32 + 64 + 3 * 3  # branch, signature, fee:gas_limit:storage_limit mutez values (+3 bytes)
        )

    def gas_limit(self, content):
        values = {
            'reveal': 10000,
            'delegation': 10000,
            'origination': self.hard_gas_limit_per_operation if content.get('script') else 10000,
            'transaction': self.hard_gas_limit_per_operation if content.get('parameters') else 10200
        }
        return values.get(content['kind'])

    def storage_limit(self, content):
        values = {
            'reveal': 0,
            'delegation': 0,
            'origination': self.hard_storage_limit_per_operation if content.get('script') else 10200,
            'transaction': self.hard_storage_limit_per_operation if content.get('parameters') else 257
        }
        return values.get(content['kind'])

    def burn_cap(self, content):
        values = {
            'reveal': 0,
            'delegation': 0,
            'origination': 257,
            'transaction': 0 if content.get('parameters') else 257
        }
        return values.get(content['kind'])
