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

    def test_now_babylonnet(self):
        contract = ContractInterface.create_from(code)
        now = format_timestamp(pytezos.now())
        res = contract.call().result(storage=0)
        self.assertEqual(now, res.storage)

    def test_now_mainnet(self):
        contract = ContractInterface.create_from(code, shell='mainnet')
        now = format_timestamp(pytezos.using('mainnet').now())
        res = contract.call().result(storage=0)
        self.assertEqual(now, res.storage)

    def test_now_zeronet(self):
        contract = ContractInterface.create_from(code, shell='zeronet')
        now = format_timestamp(pytezos.using('zeronet').now())
        res = contract.call().result(storage=0)
        self.assertEqual(now, res.storage)
