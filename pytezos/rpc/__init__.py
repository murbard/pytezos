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
        return ShellQuery(node=RpcNode(uri=self.urls[network], network=network))

    def __dir__(self):
        return list(super(RpcProvider, self).__dir__()) + list(self.urls.keys())

    def __repr__(self):
        res = [
            super(RpcProvider, self).__repr__(),
            '\nNetworks',
            *list(map(lambda x: f'.{x[0]}  # {x[1]}', self.urls.items()))
        ]
        return '\n'.join(res)


localhost = RpcProvider(
    sandboxnet='http://127.0.0.1:8732/'
)
tzkt = RpcProvider(
    mainnet='https://rpc.tzkt.io/mainnet/',
    babylonnet='https://rpc.tzkt.io/babylonnet/',
    zeronet='https://rpc.tzkt.io/zeronet/'
)

mainnet = tzkt.mainnet
babylonnet = tzkt.babylonnet
zeronet = tzkt.zeronet
