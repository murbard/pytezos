from pytezos.rpc.node import RpcQuery


class Votes(RpcQuery):

    def __init__(self, *args, **kwargs):
        super(Votes, self).__init__(
            properties=[
                'ballot_list', 'ballots', 'current_period_kind', 'current_proposal', 'current_quorum',
                'listings', 'proposals'
            ],
            *args, **kwargs)

    def roll_count(self, proposal_id) -> int:
        proposals = self.proposals()
        roll_count = next((x[1] for x in proposals if x[0] == proposal_id), 0)
        return roll_count
