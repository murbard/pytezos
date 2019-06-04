from pytezos.rpc.node import Node, RpcQuery
from pytezos.rpc.chain import ChainsQuery
from pytezos.rpc.block import Block
from pytezos.rpc.context import Context
from pytezos.rpc.helpers import HelpersMixin
from pytezos.rpc.protocol import ProtocolQuery, FetchProtocolQuery
from pytezos.rpc.injection import InjectionQuery
from pytezos.rpc.monitor import MonitorQuery
from pytezos.rpc.network import NetworkQuery
from pytezos.rpc.worker import WorkersQuery


class Shell(RpcQuery, HelpersMixin):

    def __init__(self, node):
        super(Shell, self).__init__(
            node=node,
            properties={
                'chains': ChainsQuery,
                'errors': RpcQuery,
                'injection': InjectionQuery,
                'monitor': MonitorQuery,
                'network': NetworkQuery,
                'workers': WorkersQuery
            }
        )

    @property
    def protocols(self):
        return RpcQuery(
            path=f'{self._path}/protocols',
            node=self._node,
            child_class=ProtocolQuery
        )

    @property
    def fetch_protocol(self):
        return RpcQuery(
            path=f'{self._path}/fetch_protocol',
            node=self._node,
            child_class=FetchProtocolQuery
        )

    @property
    def stats(self):
        return RpcQuery(
            path=f'{self._path}/stats',
            node=self._node,
            properties=['gc', 'memory']
        )

    # Shortcuts

    @property
    def blocks(self):
        return self.chains.main.blocks

    @property
    def head(self) -> Block:
        return self.blocks.head

    @property
    def context(self) -> Context:
        return self.head.context

    def level(self) -> int:
        return self.head.level()

    def cycle(self) -> int:
        return self.head.cycle()
