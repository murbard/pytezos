import simplejson as json
from requests import Response

from pytezos.rpc.node import RpcQuery


class MonitorResponse:

    def __init__(self, res: Response):
        self._lines = res.iter_lines()

    def __iter__(self):
        for line in self._lines:
            yield json.loads(line.decode())


class MonitorChildQuery(RpcQuery):

    def _call(self, params=None):
        return MonitorResponse(self._node.get(
            path=self._path,
            params=params,
            stream=True
        ))

    def __call__(self):
        return self._call()


class MonitorValidBlocksQuery(MonitorChildQuery):

    def __call__(self, protocol=None, next_protocol=None, chain=None):
        return self._call({
            'protocol': protocol,
            'next_protocol': next_protocol,
            'chain': chain
        })


class MonitorChainHeadsQuery(MonitorChildQuery):

    def __call__(self, next_protocol=None):
        return self._call({
            'next_protocol': next_protocol
        })


class MonitorQuery(RpcQuery):

    def __init__(self, *args, **kwargs):
        super(MonitorQuery, self).__init__(
            child_class=MonitorChildQuery,
            properties=['active_chains', 'bootstrapped', 'commit_hash', 'protocols'],
            *args, **kwargs
        )

    @property
    def heads(self):
        return RpcQuery(
            path=f'{self._path}/heads',
            node=self._node,
            child_class=MonitorChainHeadsQuery
        )

    @property
    def valid_blocks(self):
        return MonitorValidBlocksQuery(
            path=f'{self._path}/valid_blocks',
            node=self._node
        )
