from unittest import TestCase

from tests import get_data
from pytezos.michelson.converter import michelson_to_micheline, micheline_to_michelson


class PairMacroExpansionTest(TestCase):

    def test_pair_macro(self):
        source = get_data(path='macros/pair_macro/source.tz')
        expanded = get_data(path='macros/pair_macro/expanded.tz', strip=True)
        micheline = michelson_to_micheline(source)
        res = micheline_to_michelson(micheline, inline=True)
        self.assertEqual(expanded, res)
