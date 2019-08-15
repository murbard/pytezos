from pytezos.rpc import RpcProvider, localhost, mainnet, alphanet, zeronet
from pytezos.crypto import Key
from pytezos.proto import Proto
from pytezos.michelson.contract import Contract
from pytezos.client import PyTezosClient
from pytezos.operation.group import OperationGroup
from pytezos.michelson.interface import ContractInterface

pytezos = PyTezosClient()
