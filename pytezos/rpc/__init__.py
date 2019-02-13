from pytezos.rpc.chain import Chain
from pytezos.rpc.node import Node, predefined

mainnet = Chain(node=Node(predefined['mainnet'][0]))
zeronet = Chain(node=Node(predefined['zeronet'][0]))
