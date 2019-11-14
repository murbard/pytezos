from os.path import join, dirname
from unittest import TestCase
from pytezos import ContractInterface


class HelloWorldContractTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.token_v3 = ContractInterface.create_from(join(dirname(__file__), 'contract.tz'))

    def test_mint(self):
        alice = "tz1ibMpWS6n6MJn73nQHtK5f4ogyYC1z9T9z"
        val = 3
        res = self.token_v3 \
            .mint(mintOwner=alice, mintValue=val) \
            .result(
                storage={
                    "admin": alice,
                    "balances": {  },
                    "paused": False,
                    "shareType": "APPLE",
                    "totalSupply": 0
                },
                source=alice)

        self.assertEqual(val, res.big_map_diff['balances'][alice])
