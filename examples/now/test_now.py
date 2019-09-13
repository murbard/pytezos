from unittest import TestCase

from pytezos import ContractInterface, pytezos, format_timestamp

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
        now = format_timestamp(pytezos.now())
        self.assertEqual(now, res.storage)
