from unittest import TestCase

from pytezos import ContractInterface


code = """
parameter (big_map nat nat);
storage (big_map nat nat);
code { CAR ; NIL operation ; PAIR }
"""


class BigMapArgTest(TestCase):

    def test_pass_big_map_diff(self):
        ci = ContractInterface.from_michelson(code)
        res = ci.call({2: 2}).interpret(storage={1: 1})
        self.assertEqual({2: 2}, res.storage)

    def test_pass_big_map_ptr(self):
        ci = ContractInterface.from_michelson(code)
        res = ci.call(123).interpret(storage={1: 1})  # FIXME: this should fail with something like "Big_map not found"
        self.assertEqual({}, res.storage)
