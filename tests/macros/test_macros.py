# How to obtain test data:
# 1. Copy
# 2. ~/tezos-babylonnet/tezos-client
#   -P 443 -A "tezos-dev.cryptonomic-infra.tech" -S
#   originate contract papair transferring 0 from key1 running ~/macros/pair_macro.tz
#   --dry-run --burn-cap 0.411
import re
from unittest import TestCase

from tests import get_data
from pytezos.michelson.converter import michelson_to_micheline, micheline_to_michelson


class MacrosTest(TestCase):

    def assertScriptEqual(self, expected, actual):
        e = re.sub(r'[ \t\r\n\f]+', ' ', expected)
        a = re.sub(r'[ \t\r\n\f]+', ' ', actual)
        return self.assertEqual(e, a)

    def test_pair_macro(self):
        source = get_data(path='macros/pair_macro/source.tz')
        expanded = get_data(path='macros/pair_macro/expanded.tz')
        micheline = michelson_to_micheline(source)
        res = micheline_to_michelson(micheline)
        self.assertScriptEqual(expanded, res)

    def test_unpair_macro(self):
        source = get_data(path='macros/unpair_macro/source.tz')
        expanded = get_data(path='macros/unpair_macro/expanded.tz')
        micheline = michelson_to_micheline(source)
        res = micheline_to_michelson(micheline)
        self.assertScriptEqual(expanded, res)

    def test_set_cadadr_macro(self):
        source = get_data(path='macros/set_cadadr/source.tz')
        expanded = get_data(path='macros/set_cadadr/expanded.tz')
        micheline = michelson_to_micheline(source)
        res = micheline_to_michelson(micheline)
        self.assertScriptEqual(expanded, res)
