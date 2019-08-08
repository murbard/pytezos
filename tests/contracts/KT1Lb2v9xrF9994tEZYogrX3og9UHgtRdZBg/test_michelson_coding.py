from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import micheline_to_michelson, michelson_to_micheline


class MichelsonCodingTestKT1Lb2(TestCase):
    
    def setUp(self):
        self.maxDiff = None

    def test_michelson_parse_code_KT1Lb2(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/code_KT1Lb2.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/code_KT1Lb2.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_code_KT1Lb2(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/code_KT1Lb2.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/code_KT1Lb2.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_code_KT1Lb2(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/code_KT1Lb2.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_storage_KT1Lb2(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/storage_KT1Lb2.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/storage_KT1Lb2.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_storage_KT1Lb2(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/storage_KT1Lb2.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/storage_KT1Lb2.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_storage_KT1Lb2(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/storage_KT1Lb2.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_ooso91(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_ooso91.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_ooso91.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_ooso91(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_ooso91.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_ooso91.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_ooso91(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_ooso91.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_opMCQC(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_opMCQC.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_opMCQC.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_opMCQC(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_opMCQC.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_opMCQC.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_opMCQC(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_opMCQC.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_ooYrJr(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_ooYrJr.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_ooYrJr.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_ooYrJr(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_ooYrJr.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_ooYrJr.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_ooYrJr(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_ooYrJr.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_opJ56P(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_opJ56P.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_opJ56P.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_opJ56P(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_opJ56P.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_opJ56P.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_opJ56P(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_opJ56P.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_oovBBY(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_oovBBY.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_oovBBY.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_oovBBY(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_oovBBY.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_oovBBY.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_oovBBY(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_oovBBY.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_op6A4x(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_op6A4x.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_op6A4x.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_op6A4x(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_op6A4x.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_op6A4x.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_op6A4x(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_op6A4x.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_oo6me4(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_oo6me4.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_oo6me4.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_oo6me4(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_oo6me4.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_oo6me4.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_oo6me4(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_oo6me4.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_ooonw4(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_ooonw4.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_ooonw4.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_ooonw4(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_ooonw4.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_ooonw4.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_ooonw4(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_ooonw4.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_oo1Wog(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_oo1Wog.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_oo1Wog.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_oo1Wog(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_oo1Wog.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_oo1Wog.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_oo1Wog(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_oo1Wog.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_ookQWr(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_ookQWr.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_ookQWr.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_ookQWr(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_ookQWr.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_ookQWr.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_ookQWr(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1Lb2v9xrF9994tEZYogrX3og9UHgtRdZBg/parameter_ookQWr.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)
