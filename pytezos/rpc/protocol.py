import pendulum
from pendulum.parsing.exceptions import ParserError
from datetime import datetime

from pytezos.rpc.query import RpcQuery, get_attr_docstring
from pytezos.encoding import is_bh
from pytezos.entities.block import BlockHeader, Block


def to_timestamp(v):
    try:
        v = pendulum.parse(v)
    except ParserError:
        pass
    if isinstance(v, datetime):
        v = int(v.timestamp())
    return v


class BlockSliceQuery(RpcQuery):

    def __init__(self, length, head, **kwargs):
        super(BlockSliceQuery, self).__init__(**kwargs)
        self._length = length
        self._head = head

    def __repr__(self):
        return f'()\n{get_attr_docstring(BlockSliceQuery, "__call__")}'

    def __call__(self):
        """
        Slice
        :return: Array of block hashes
        """
        header = self[self._head].header()
        if self._length < 0:
            self._length += header['level']

        return super(BlockSliceQuery, self).__call__(length=self._length, head=header['hash'])


class BlocksQuery(RpcQuery, path='/chains/{}/blocks'):

    def __call__(self, length=1, head=None, min_date=None):
        """
        Lists known heads of the blockchain sorted with decreasing fitness.
        Optional arguments allows to returns the list of predecessors for known heads
        or the list of predecessors for a given list of blocks.
        :param length: The requested number of predecessors to returns (per requested head).
        :param head: An empty argument requests blocks from the current heads.
        A non empty list allow to request specific fragment of the chain.
        :param min_date: When `min_date` is provided, heads with a timestamp before `min_date` are filtered out
        :return: Array of arrays of block hashes
        """
        if isinstance(head, str) and not is_bh(head):
            head = self.__getitem__(head).calculate_hash()

        if min_date and not isinstance(min_date, int):
            min_date = to_timestamp(min_date)

        return super(BlocksQuery, self).__call__(
            length=length, head=head, min_date=min_date)

    def __getitem__(self, block_id):
        """
        Advanced indexing
        :param block_id: integer
        :return:
        """
        if isinstance(block_id, slice):
            if not isinstance(block_id.start, int):
                raise NotImplementedError('Slice start should be an integer.')

            if block_id.stop is None:
                head = 'head'
            elif isinstance(block_id.stop, int):
                if block_id.stop < 0:
                    head = f'head~{abs(block_id.stop)}'
                else:
                    head = block_id.stop
            else:
                raise NotImplementedError('Slice stop can be an integer or None.')

            if block_id.start < 0:
                length = abs(block_id.start)
                if isinstance(block_id.stop, int) and block_id.stop < 0:
                    length -= abs(block_id.stop)
            else:
                length = -block_id.start

            return BlockSliceQuery(
                length=length,
                head=head,
                node=self._node,
                path=self._path,
                params=self._params
            )

        return super(BlocksQuery, self).__getitem__(block_id)


class BlockQuery(RpcQuery, path='/chains/{}/blocks/{}'):

    def __init__(self, *args, **kwargs):
        super(BlockQuery, self).__init__(*args, **kwargs)
        self._caching = self._caching or 'head' not in self._params

    @property
    def predecessor(self):
        """
        Queries previous block hash from node and returns new query.
        :return: `BlockQuery` instance
        """
        return self._parent[self.header()['predecessor']]

    @property
    def baker(self):
        return self.context.contracts[self.metadata()['baker']]

    def get_level(self) -> int:
        """
        Level for this block from metadata.
        :return: Integer
        """
        return self.metadata()['level']['level']

    def get_cycle(self) -> int:
        """
        Cycle for this block from metadata.
        :return: Integer
        """
        return self.metadata()['level']['cycle']

    def decode(self):
        """
        TODO
        :return:
        """
        return Block(self())


class BlockHeaderQuery(RpcQuery, path='/chains/{}/blocks/{}/header'):

    def decode(self):
        """
        Converts JSON interpretation into the block header entity.
        :return: `BlockHeader` instance
        """
        return BlockHeader(self())


class ContractQuery(RpcQuery, path='/chains/{}/blocks/{}/context/contracts/{}'):

    def decode(self):
        """

        :return:
        """
        return self()

    def get_public_key(self):
        """
        Retrieves the owner's public key
        :return: base58 encoded public key
        """
        pkh = self._params[-1]
        if pkh.startswith('KT'):
            pkh = self.manager_key().get('manager')

        pk = self._parent[pkh].manager_key().get('key')
        if not pk:
            raise ValueError('Public key is not revealed.')

        return pk


class BigMapGetQuery(RpcQuery, path='/chains/{}/blocks/{}/context/contracts/{}/big_map_get'):

    def post(self, key, key_type, key_prim):
        """
        Access the value associated with a key in the big map storage  of the contract.
        :param key:
        :param key_type: Provided key encoding, e.g. "string", "bytes" for hex-encoded string, "int"
        :param key_prim: Expected high-level data type, e.g. "address", "nat", "mutez" (see storage section in code)
        :return: Micheline expression
        """
        return self._post(json={
            'key': {key_type: key},
            'type': {'prim': key_prim}
        })


class ContextRawBytesQuery(RpcQuery, path='/chains/{}/blocks/{}/context/raw/bytes'):

    def __call__(self, depth=1):
        """
        Returns the raw context.
        :param depth: default is 1
        :return:
        """
        return super(ContextRawBytesQuery, self).__call__(depth=depth)


class ContextSeedQuery(RpcQuery, path='/chains/{}/blocks/{}/context/seed'):

    def post(self):
        return self._post()


class OperationListListQuery(RpcQuery, path=['/chains/{}/blocks/{}/operation_hashes',
                                             '/chains/{}/blocks/{}/operations']):

    @property
    def endorsements(self):
        return self[0]

    @property
    def votes(self):
        return self[1]

    @property
    def anonymous(self):
        return self[2]

    @property
    def managers(self):
        return self[3]


class OperationQuery(RpcQuery, path='/chains/{}/blocks/{}/operations/{}/{}'):

    def decode(self):
        return self()


class ProposalQuery(RpcQuery, path='/chains/{}/blocks/{}/votes/proposals/{}'):
    """
    Extended query
    """
    def __call__(self):
        """
        Roll count for this proposal
        :return: integer
        """
        proposals = self._parent.proposals()
        proposal_id = self._params[-1]
        roll_count = next((x[1] for x in proposals if x[0] == proposal_id), 0)
        return roll_count


class ProposalsQuery(RpcQuery, path='/chains/{}/blocks/{}/votes/proposals'):

    def __getitem__(self, proposal_id):
        """
        Roll count for the selected proposal
        :param proposal_id: Base58-encoded proposal ID
        :return: Integer
        """
        return self._spawn_query(
            path=f'{self._path}/proposal_id',
            params=self._params + [proposal_id]
        )

    def __repr__(self):
        docstring = super(ProposalsQuery, self).__repr__()
        docstring += f'[]\n{ProposalsQuery.__getitem__.__doc__}'
        return docstring
