from unittest import TestCase

from tests import get_data
from pytezos.michelson.converter import michelson_to_micheline


class TestAtticAccountsParse(TestCase):

    def test_parser(self):
        data = get_data('macros/attic_accounts/accounts.tz', strip=False)
        res = michelson_to_micheline(data)
        self.assertIsNotNone(res)
