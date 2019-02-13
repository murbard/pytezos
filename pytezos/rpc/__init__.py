from pytezos.rpc.shell import Shell
from pytezos.rpc.node import Node, TEZRPC_MAINNET, TZSCAN_ZERONET

mainnet = Shell(Node(TEZRPC_MAINNET))
zeronet = Shell(Node(TZSCAN_ZERONET))
