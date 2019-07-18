class Content:

    @classmethod
    def endorsement(cls, level: int):
        """
        Endorse a block
        :param level: Endorsed level
        :return: Operation content
        """
        return {
            'kind': 'endorsement',
            'level': level
        }

    @classmethod
    def seed_nonce_revelation(cls, level: int, nonce):
        """
        Reveal the nonce committeOperationd in the previous cycle.
        More info https://tezos.stackexchange.com/questions/567/what-are-nonce-revelations
        :param level: When nonce hash was committed
        :param nonce: Hex string
        :return: Operation content
        """
        return {
            'kind': 'seed_nonce_revelation',
            'level': level,
            'nonce': nonce
        }

    @classmethod
    def double_endorsement_evidence(cls, op1: dict, op2: dict):
        """
        Provide evidence of double endorsement (endorsing two different blocks at the same block height).
        :param op1: Inline endorsement {
            "branch": $block_hash,
            "operations": {
                "kind": "endorsement",
                "level": integer ∈ [-2^31-2, 2^31+2]
            },
            "signature"?: $Signature
        }
        :param op2: Inline endorsement
        :return: Operation content
        """
        return {
            'kind': 'double_endorsement_evidence',
            'op1': op1,
            'op2': op2
        }

    @classmethod
    def double_baking_evidence(cls, bh1, bh2):
        """
        Provide evidence of double baking (two different blocks at the same height).
        :param bh1: First block hash
        :param bh2: Second block hash
        :return: Operation content
        """
        return {
            'kind': 'double_baking_evidence',
            'bh1': bh1,
            'bh2': bh2
        }

    @classmethod
    def activate_account(cls, pkh, activation_code):
        """
        Activate recommended allocations for contributions to the TF fundraiser.
        More info https://activate.tezos.com/
        :param pkh: Public key hash
        :param activation_code: Secret code from pdf
        :return: Operation content
        """
        return {
            'kind': 'activate_account',
            'pkh': pkh,
            'secret': activation_code
        }

    @classmethod
    def proposals(cls, proposals: list,
                  source=None, period=None):
        """
        Submit and/or upvote proposals to amend the protocol.
        Can only be submitted during a proposal period.
        More info https://tezos.gitlab.io/master/whitedoc/voting.html
        :param proposals: List of proposal hashes
        :param source: Public key hash (of the signatory), leave none for autocomplete
        :param period: Number of the current voting period, leave none for autocomplete
        :return: Operation content
        """
        return {
            'kind': 'proposals',
            'source': source,
            'period': period,
            'proposals': proposals
        }

    @classmethod
    def ballot(cls, proposal, ballot,
               source=None, period=None):
        """
        Vote for a proposal in a given voting period.
        Can only be submitted during Testing_vote or Promotion_vote periods, and only once per period.
        More info https://tezos.gitlab.io/master/whitedoc/voting.html
        :param proposal: Hash of the proposal
        :param ballot: 'Yay', 'Nay' or 'Pass'
        :param source: Public key hash (of the signatory), leave none for autocomplete
        :param period: Number of the current voting period, leave none for autocomplete
        :return:
        """
        return {
            'kind': 'ballot',
            'source': source,
            'period': period,
            'proposal': proposal,
            'ballot': ballot
        }

    @classmethod
    def reveal(cls, public_key,
               source=None, counter=None, fee=None, gas_limit=None, storage_limit=None):
        """
        Reveal the public key associated with a tz address.
        :param public_key: Public key to reveal, Base58 encoded
        :param source:
        :param counter: Current michelson counter, leave none for autocomplete
        (More info https://tezos.stackexchange.com/questions/632/how-counter-grows)
        :param fee: Leave none for autocomplete
        :param gas_limit: Leave none for autocomplete
        :param storage_limit: Leave none for autocomplete
        :return:
        """
        return {
            'kind': 'reveal',
            'source': source,
            'fee': fee,
            'counter': counter,
            'gas_limit': gas_limit,
            'storage_limit': storage_limit,
            'public_key': public_key
        }

    @classmethod
    def transaction(cls, destination, amount: int, parameters=None,
                    source=None, counter=None, fee=None, gas_limit=None, storage_limit=None):
        """
        Transfer tezzies to an account (implicit or originated).
        If the receiver is an originated account (KT1…), then optional parameters may be passed.
        :param source:
        :param destination:
        :param amount:
        :param counter:
        :param parameters:
        :param fee:
        :param gas_limit:
        :param storage_limit:
        :return: Operation content
        """
        return {
            'kind': 'transaction',
            'source': source,
            'fee': fee,
            'counter': counter,
            'gas_limit': gas_limit,
            'storage_limit': storage_limit,
            'amount': amount,
            'destination': destination,
            'parameters': parameters
        }

    @classmethod
    def origination(cls, manager_pubkey=None, script=None,
                    source=None, counter=None, fee=None, gas_limit=None, storage_limit=None):
        """
        :param manager_pubkey:
        :param script:
        :param source:
        :param counter:
        :param fee:
        :param gas_limit:
        :param storage_limit:
        :return:
        """
        return {
            'kind': 'transaction',
            'source': source,
            'fee': fee,
            'counter': counter,
            'gas_limit': gas_limit,
            'storage_limit': storage_limit,
            'manager_pubkey': manager_pubkey,
            'balance': 0,
            'script': script
        }

    @classmethod
    def delegation(cls, delegate,
                   source=None, counter=None, fee=None, gas_limit=None, storage_limit=None):
        """

        :param delegate:
        :param source:
        :param counter:
        :param fee:
        :param gas_limit:
        :param storage_limit:
        :return:
        """
        return {
            'kind': 'delegation',
            'source': source,
            'fee': fee,
            'counter': counter,
            'gas_limit': gas_limit,
            'storage_limit': storage_limit,
            'delegate': delegate
        }
