from pytezos.rpc import RpcProvider, mainnet, alphanet, zeronet, ShellQuery
from pytezos.crypto import Key
from pytezos.client import PyTezosClient
from pytezos.operation.group import OperationGroup
from pytezos.michelson.contract import Contract
from pytezos.michelson.interface import ContractInterface

pytezos = PyTezosClient()
