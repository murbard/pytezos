from unittest import TestCase

from tests import get_data
from pytezos.michelson.converter import michelson_to_micheline


data = """
"""


class TestAtticAccountsParse(TestCase):

    def test_parser(self):
        #data = get_data('macros/attic_accounts/accounts.tz', strip=False)
        res = michelson_to_micheline("PAPPAIIR %x1 %x2 %x3 %x4")
        self.assertIsNotNone(res)
