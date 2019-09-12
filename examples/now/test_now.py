from unittest import TestCase
from datetime import datetime

from pytezos import ContractInterface, pytezos

code = """
parameter unit;
storage timestamp;
code { DROP ;
       NOW ;
       NIL operation ;
       PAIR }
"""


class TimeContractTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ci = ContractInterface.create_from(code)

    def test_now(self):
        res = self.ci.call().result(storage=0)
        now = int(datetime.strptime(res.storage, '%Y-%m-%dT%H:%M:%SZ').timestamp())
        self.assertAlmostEqual(pytezos.now(), now, delta=1)
