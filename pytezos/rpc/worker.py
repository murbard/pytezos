from pytezos.rpc.node import RpcQuery


class ChainValidatorQuery(RpcQuery):

    def __init__(self, *args, **kwargs):
        super(ChainValidatorQuery, self).__init__(
            properties=['peers_validators'],
            *args, **kwargs
        )


class WorkersQuery(RpcQuery):

    def __init__(self, *args, **kwargs):
        super(WorkersQuery, self).__init__(
            properties=['block_validator', 'prevalidators'],
            *args, **kwargs
        )

    @property
    def chain_validators(self):
        return RpcQuery(
            path=f'{self._path}/chain_validators',
            node=self._node,
            child_class=ChainValidatorQuery
        )
