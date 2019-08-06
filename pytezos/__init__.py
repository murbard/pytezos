from pytezos.rpc import create_shell
from pytezos.crypto import Key
from pytezos.client import PyTezosClient

local = create_shell('https://127.0.0.1:8732/')

mainnet_tzscan = create_shell('https://mainnet-node.tzscan.io/')
alphanet_tzscan = create_shell('https://alphanet-node.tzscan.io/')
zeronet_tzscan = create_shell('https://zeronet-node.tzscan.io/')

mainnet_tzbeta = create_shell('https://rpc.tzbeta.net/')
alphanet_tzbeta = create_shell('https://rpcalpha.tzbeta.net/')

mainnet_tezbox = create_shell('https://rpc.tezrpc.me/')
alphanet_tezbox = create_shell('https://alphanet.tezrpc.me/')

mainnet_cryptonomic = create_shell('https://tezos-prod.cryptonomic-infra.tech/')
alphanet_cryptonomic = create_shell('https://tezos-dev.cryptonomic-infra.tech/')

mainnet = mainnet_cryptonomic
alphanet = alphanet_cryptonomic
zeronet = zeronet_tzscan

please_use_with_care = Key.from_encoded_key('edsk33N474hxzA4sKeWVM6iuGNGDpX2mGwHNxEA4UbWS8sW3Ta3NKH')
pytezos = PyTezosClient(shell=alphanet, key=please_use_with_care)
