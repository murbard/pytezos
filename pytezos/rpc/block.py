from pytezos.rpc.node import Node
from pytezos.rpc.context import Context


class BlockHeader:

    def __init__(self, block_id='head', chain_id='main', node=Node()):
        self._block_id = block_id
        self._chain_id = chain_id
        self._node = node
        self._path = f'chains/{chain_id}/blocks/{block_id}/header'

    def __repr__(self):
        return self._path

    def __call__(self, *args, **kwargs):
        return self._node.get(self._path)

    @property
    def raw(self):
        return self._node.get(f'{self._path}/raw')

    @property
    def shell(self):
        return self._node.get(f'{self._path}/shell')

    @property
    def protocol_data(self):
        return self._node.get(f'{self._path}/protocol_data')

    @property
    def protocol_data_raw(self):
        return self._node.get(f'{self._path}/protocol_data/raw')


class OperationsList:

    def __init__(self, block_id='head', chain_id='main', node=Node()):
        self._block_id = block_id
        self._chain_id = chain_id
        self._node = node
        self._path = f'chains/{chain_id}/blocks/{block_id}/operations'

    def __repr__(self):
        return self._path

    def __call__(self, *args, **kwargs):
        return self._node.get(self._path)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._node.get(f'{self._path}/{item}')
        elif isinstance(item, tuple):
            return self._node.get(f'{self._path}/{item[0]}/{item[1]}')
        raise KeyError


class Block:
    """
    See https://tezos.gitlab.io/mainnet/whitedoc/proof_of_stake.html
    """
    __dyn_attrs__ = ['hash', 'metadata']

    def __init__(self, block_id='head', chain_id='main', node=Node()):
        self._block_id = block_id
        self._chain_id = chain_id
        self._node = node
        self._path = f'chains/{chain_id}/blocks/{block_id}'

    def __repr__(self):
        return self._path

    def __call__(self, *args, **kwargs):
        return self._node.get(self._path)

    def __dir__(self):
        return sorted(super(Block, self).__dir__() + self.__dyn_attrs__)

    def __getattr__(self, item):
        if item in self.__dyn_attrs__:
            return self._node.get(f'{self._path}/{item}')
        raise AttributeError(item)

    @property
    def header(self) -> BlockHeader:
        return BlockHeader(self._block_id, self._chain_id, self._node)

    @property
    def operations(self) -> OperationsList:
        return OperationsList(self._block_id, self._chain_id, self._node)

    @property
    def context(self) -> Context:
        return Context(self._block_id, self._chain_id, self._node)

    def capture(self):
        """
        Returns fixed-hash block, useful for aliases, like head, head~1, etc.
        :return: Block instance with hash initialized
        """
        return Block(self.hash, self._chain_id, self._node)
