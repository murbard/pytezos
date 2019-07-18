from pytezos.rpc.shell import *
from pytezos.rpc.protocol import *
from pytezos.rpc.helpers import *
from pytezos.rpc.node import RpcNode


def create_shell(uri):
    return ShellQuery(node=RpcNode(uri))


mainnet_local = create_shell('https://127.0.0.1:8732/')
alphanet_local = create_shell('https://127.0.0.1:8732/')
zeronet_local = create_shell('https://127.0.0.1:8732/')

mainnet_tzscan = create_shell('https://mainnet-node.tzscan.io/')
alphanet_tzscan = create_shell('https://alphanet-node.tzscan.io/')
zeronet_tzscan = create_shell('https://zeronet-node.tzscan.io/')

mainnet_tzbeta = create_shell('https://rpc.tzbeta.net/')
alphanet_tzbeta = create_shell('https://rpcalpha.tzbeta.net/')

mainnet_tezbox = create_shell('https://rpc.tezrpc.me/')
alphanet_tezbox = create_shell('https://alphanet.tezrpc.me/')

cryptonomic_alphanet = create_shell('https://tezos-dev.cryptonomic-infra.tech/')

mainnet = mainnet_tzscan
alphanet = cryptonomic_alphanet
zeronet = zeronet_tzscan
