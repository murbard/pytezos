import requests
import simplejson as json
from functools import lru_cache
from binascii import hexlify

from pytezos.encoding import base58_decode
from pytezos.rpc.query import RpcQuery, get_attr_docstring


class ShellQuery(RpcQuery, path=''):

    @property
    def blocks(self):
        return self.chains.main.blocks

    @property
    def head(self):
        return self.blocks.head

    @property
    @lru_cache(maxsize=None)
    def block(self):
        """
        Cached head block, useful if you just want to explore things.
        :return: `BlockQuery`
        """
        return self.blocks[self.head.hash()]


class ChainQuery(RpcQuery, path='/chains/{}'):

    def get_watermark(self):
        """
        Chain watermark
        :return: Hex encoded value
        """
        data = self.chain_id()
        return hexlify(base58_decode(data.encode())).decode()


class InvalidBlockQuery(RpcQuery, path='/chains/{}/invalid_blocks/{}'):

    def delete(self):
        return self._delete()


class MempoolQuery(RpcQuery, path='/chains/{}/mempool'):

    def post(self, configuration):
        """
        :param configuration: a JSON dictionary, known keys are `minimal_fees`, `minimal_nanotez_per_gas_unit`,
        `minimal_nanotez_per_byte`
        """
        return self._post(json=configuration)


class PendingOperationsQuery(RpcQuery, path='/chains/{}/mempool/pending_operations'):

    def applied(self):
        return self()['applied']

    def refused(self):
        return self()['refused']

    def branch_refused(self):
        return self()['branch_refused']

    def branch_delayed(self):
        return self()['branch_delayed']

    def unprocessed(self):
        return self()['unprocessed']


class DescribeQuery(RpcQuery, path='/describe'):

    def __call__(self, recurse=True):
        """
        RPCs documentation and input/output schema.
        :param recurse: Show information for child elements, default is True.
        In some cases doesn't work without this flag.
        :return: Object
        """
        return super(DescribeQuery, self).__call__(recurse=recurse)

    def __repr__(self):
        docstring = get_attr_docstring(DescribeQuery, '__call__')
        additional = 'Can be followed by any path:\n.chains\n.network.connections\netc\n'
        return f'Path\n/describe\n\n(){docstring}\n{additional}'


class BlockInjectionQuery(RpcQuery, path='/injection/block'):

    def post(self, block, _async=False, force=False, chain=None):
        """
        Inject a block in the node and broadcast it.
        The `operations` embedded in `blockHeader` might be pre-validated using a contextual RPCs from the latest block
        (e.g. '/blocks/head/context/preapply').
        :param block: Json input:
        {
            "data": <hex-encoded block header>,
            "operations": [ [ {
                "branch": <block_hash>,
                "data": <hex-encoded operation>
            } ... ] ... ]
        }
        :param _async: By default, the RPC will wait for the block to be validated before answering,
        set True if you don't want to.
        :param force:
        :param chain: Optionally you can specify the chain
        :return: ID of the block
        """
        return self._post(
            params={
                'async': _async,
                'force': force,
                'chain': chain
            },
            json=block
        )


class OperationInjectionQuery(RpcQuery, path='/injection/operation'):

    def post(self, operation, _async=False, chain=None):
        """
        Inject an operation in node and broadcast it.
        The `signedOperationContents` should be constructed using a contextual RPCs from the latest block
        and signed by the client.
        :param operation: Hex-encoded operation data
        :param _async: By default, the RPC will wait for the operation to be (pre-)validated before answering,
        set True if you don't want to.
        :param chain: Optionally you can specify the chain
        :return: ID of the operation
        """
        return self._post(
            params={
                'async': _async,
                'chain': chain
            },
            json=operation
        )


class ProtocolInjectionQuery(RpcQuery, path='/injection/protocol'):

    def post(self, protocol, _async=False, force=False):
        """
        Inject a protocol in node.
        :param protocol: Json input:
        {
            "expected_env_version": <integer>,
            "components": [{
                "name": <unistring>,
                "interface"?: <hex-encoded data>,
                "implementation": <hex-encoded data> }
                 ...
            ]}
        }
        :param _async:
        :param force:
        :return: ID of the protocol
        """
        return self._post(
            params={
                'async': _async,
                'force': force
            },
            json=protocol
        )


class ResponseGenerator:

    def __init__(self, res: requests.Response):
        self._lines = res.iter_lines()

    def __iter__(self):
        for line in self._lines:
            yield json.loads(line.decode())


class MonitorQuery(RpcQuery, path=['/monitor/active_chains',
                                   '/monitor/bootstrapped',
                                   '/monitor/commit_hash',
                                   '/monitor/heads/{}',
                                   '/monitor/protocols',
                                   '/monitor/valid_blocks']):

    def __call__(self, *args, **kwargs):
        return ResponseGenerator(self._node.request(
            method='GET',
            path=self._query_path,
            params=kwargs,
            stream=True
        ))

    def __repr__(self):
        docstring = super(MonitorQuery, self).__repr__()
        docstring += '\nNOTE\nReturned object is a generator.'
        return docstring


class ConnectionQuery(RpcQuery, path='/network/connections/{}'):

    def delete(self, wait=False):
        return self._delete(params=dict(wait=wait))


class NetworkItems(RpcQuery, path=['/network/peers', '/network/points']):

    def __call__(self, _filter=None):
        return self._get(params={'filter': _filter})


class NetworkLogQuery(RpcQuery, path=['/network/peers/{}/log', '/network/points/{}/log']):
    pass
