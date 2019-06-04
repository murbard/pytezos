from pytezos.rpc.node import RpcQuery


class InjectionBlockQuery(RpcQuery):

    def post(self, block, _async=False, force=False, chain=None):
        return self._node.post(
            path=self._path,
            params={
                'async': _async,
                'force': force,
                'chain': chain
            },
            json=block
        )


class InjectionOperationQuery(RpcQuery):

    def post(self, operation, _async=False, chain=None):
        return self._node.post(
            path=self._path,
            params={
                'async': _async,
                'chain': chain
            },
            json=operation
        )


class InjectionProtocolQuery(RpcQuery):

    def post(self, protocol, _async=False, force=False):
        return self._node.post(
            path=self._path,
            params={
                'async': _async,
                'force': force
            },
            json=protocol
        )


class InjectionQuery(RpcQuery):

    def __init__(self, *args, **kwargs):
        super(InjectionQuery, self).__init__(
            properties={
                'block': InjectionBlockQuery,
                'operation': InjectionOperationQuery,
                'protocol': InjectionProtocolQuery
            },
            *args, **kwargs
        )
