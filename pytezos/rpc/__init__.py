from pytezos.rpc.shell import *
from pytezos.rpc.protocol import *
from pytezos.rpc.helpers import *
from pytezos.rpc.search import *
from pytezos.rpc.node import RpcNode


class RpcProvider:

    def __init__(self, **urls):
        self.urls = urls

    @lru_cache(maxsize=None)
    def __getattr__(self, network) -> ShellQuery:
        return ShellQuery(node=RpcNode(self.urls[network]))

    def __dir__(self):
        return list(super(RpcProvider, self).__dir__()) + list(self.urls.keys())


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
