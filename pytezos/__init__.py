from pytezos.rpc import RpcProvider
from pytezos.crypto import Key
from pytezos.client import PyTezosClient


localhost = RpcProvider(
    mainnet='https://127.0.0.1:8732/',
    alphanet='https://127.0.0.1:8732/',
    zeronet='https://127.0.0.1:8732/'
)
tzscan = RpcProvider(
    mainnet='https://mainnet-node.tzscan.io/',
    alphanet='https://alphanet-node.tzscan.io/',
    zeronet='https://zeronet-node.tzscan.io/'
)
tzbeta = RpcProvider(
    mainnet='https://rpc.tzbeta.net/',
    alphanet='https://rpcalpha.tzbeta.net/'
)
tezbox = RpcProvider(
    mainnet='https://rpc.tezrpc.me/',
    alphanet='https://alphanet.tezrpc.me/'
)
cryptonomic = RpcProvider(
    mainnet='https://tezos-prod.cryptonomic-infra.tech/',
    alphanet='https://tezos-dev.cryptonomic-infra.tech/'
)
tulip = RpcProvider(
    mainnet='https://rpc.tulip.tools/mainnet/',
    alphanet='https://rpc.tulip.tools/alphanet/',
    zeronet='https://rpc.tulip.tools/zeronet/'
)

mainnet = tzbeta.mainnet
alphanet = cryptonomic.alphanet
zeronet = tzscan.zeronet

please_use_with_care = Key.from_encoded_key('edsk33N474hxzA4sKeWVM6iuGNGDpX2mGwHNxEA4UbWS8sW3Ta3NKH')

pytezos = PyTezosClient(shell=alphanet, key=please_use_with_care)
