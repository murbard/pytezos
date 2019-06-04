from pytezos.rpc.shell import Shell
from pytezos.rpc.node import Node

local_mainnet = Shell(Node('https://127.0.0.1:8732/'))
local_alphanet = Shell(Node('https://127.0.0.1:8732/'))
local_zeronet = Shell(Node('https://127.0.0.1:8732/'))

tzscan_mainnet = Shell(Node('https://mainnet-node.tzscan.io/'))
tzscan_alphanet = Shell(Node('https://alphanet-node.tzscan.io/'))
tzscan_zeronet = Shell(Node('https://zeronet-node.tzscan.io/'))

tzbeta_mainnet = Shell(Node('https://rpc.tzbeta.net/'))
tzbeta_alphanet = Shell(Node('https://rpcalpha.tzbeta.net/'))

tezbox_mainnet = Shell(Node('https://rpc.tezrpc.me/'))
tezbox_alphanet = Shell(Node('https://alphanet.tezrpc.me/'))

mainnet = tzscan_mainnet
alphanet = tzscan_alphanet
zeronet = tzscan_zeronet
