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
