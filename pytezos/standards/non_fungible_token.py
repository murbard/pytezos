from pytezos.michelson.contract import Contract, ContractParameter, ContractStorage
from pytezos.michelson.micheline import michelson_to_micheline

parameter_tz = """
parameter 
    (or (or (nat %burn :token_id) (pair %mint (address %owner) (nat %token_id)))
        (pair %transfer (address %destination) (nat %token_id)))
"""
storage_tz = "storage (map nat address)"

parameter = ContractParameter(michelson_to_micheline(parameter_tz))
storage = ContractStorage(michelson_to_micheline(storage_tz))


class NonFungibleTokenImpl(Contract):

    @property
    def parameter(self) -> ContractParameter:
        return parameter

    @property
    def storage(self) -> ContractStorage:
        return storage
