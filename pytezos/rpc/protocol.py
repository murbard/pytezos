from pytezos.rpc.node import RpcQuery
from pytezos.entities.protocol import Protocol


class ProtocolQuery(RpcQuery):

    def to_protocol(self) -> Protocol:
        return Protocol(self())


class FetchProtocolQuery(RpcQuery):
    pass
