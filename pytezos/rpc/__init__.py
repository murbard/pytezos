from pytezos.rpc.shell import Shell
from pytezos.rpc.node import Node, public_nodes

mainnet = Shell(Node(public_nodes['mainnet'][0]))
alphanet = Shell(Node(public_nodes['alphanet'][0]))
zeronet = Shell(Node(public_nodes['zeronet'][0]))
