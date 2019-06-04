from pytezos.rpc.node import RpcQuery


class ConnectionQuery(RpcQuery):

    def delete(self, wait=False):
        return self._node.delete(
            path=self._path,
            params={'wait': wait}
        )


class NetworkPeerQuery(RpcQuery):

    def __init__(self, *args, **kwargs):
        super(NetworkPeerQuery, self).__init__(
            properties=['ban', 'banned', 'log', 'trust', 'unban', 'untrust'],
            *args, **kwargs
        )


class NetworkPointQuery(RpcQuery):

    def __init__(self, *args, **kwargs):
        super(NetworkPointQuery, self).__init__(
            properties=['ban', 'banned', 'log', 'trust', 'unban', 'untrust'],
            *args, **kwargs
        )

    def put(self, timeout=None):
        return self._node.put(
            path=self._path,
            params={'timeout': timeout}
        )


class NetworkFilter(RpcQuery):

    def __call__(self, _filter=None):
        return self._node.get(
            path=self._path,
            params={'filter': _filter}
        )


class NetworkQuery(RpcQuery):

    def __init__(self, *args, **kwargs):
        super(NetworkQuery, self).__init__(
            properties=['log', 'self', 'stat', 'version', 'versions'],
            *args, **kwargs
        )

    @property
    def connections(self):
        return RpcQuery(
            path=f'{self._path}/connections',
            node=self._node,
            child_class=ConnectionQuery
        )

    @property
    def greylist(self):
        return RpcQuery(
            path=f'{self._path}/greylist',
            node=self._node,
            properties=['clear']
        )

    @property
    def peers(self):
        return NetworkFilter(
            path=f'{self._path}/peers',
            node=self._node,
            child_class=NetworkPeerQuery
        )

    @property
    def points(self):
        return NetworkFilter(
            path=f'{self._path}/points',
            node=self._node,
            child_class=NetworkPointQuery
        )
