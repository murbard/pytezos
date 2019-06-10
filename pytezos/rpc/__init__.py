from pytezos.rpc.shell import *
from pytezos.rpc.protocol import *
from pytezos.rpc.helpers import *
from pytezos.rpc.node import RpcNode


def create_shell(uri):
    return ShellQuery(node=RpcNode(uri))


local_mainnet = create_shell('https://127.0.0.1:8732/')
local_alphanet = create_shell('https://127.0.0.1:8732/')
local_zeronet = create_shell('https://127.0.0.1:8732/')

tzscan_mainnet = create_shell('https://mainnet-node.tzscan.io/')
tzscan_alphanet = create_shell('https://alphanet-node.tzscan.io/')
tzscan_zeronet = create_shell('https://zeronet-node.tzscan.io/')

tzbeta_mainnet = create_shell('https://rpc.tzbeta.net/')
tzbeta_alphanet = create_shell('https://rpcalpha.tzbeta.net/')

tezbox_mainnet = create_shell('https://rpc.tezrpc.me/')
tezbox_alphanet = create_shell('https://alphanet.tezrpc.me/')

mainnet = tzscan_mainnet
alphanet = tzscan_alphanet
zeronet = tzscan_zeronet
