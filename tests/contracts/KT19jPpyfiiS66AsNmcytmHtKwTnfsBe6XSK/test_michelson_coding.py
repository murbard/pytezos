from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import micheline_to_michelson, michelson_to_micheline


class MichelsonCodingTestKT19jP(TestCase):
    
    def setUp(self):
        self.maxDiff = None

    def test_michelson_parse_code_KT19jP(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/code_KT19jP.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/code_KT19jP.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_code_KT19jP(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/code_KT19jP.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/code_KT19jP.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_code_KT19jP(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/code_KT19jP.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_storage_KT19jP(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/storage_KT19jP.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/storage_KT19jP.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_storage_KT19jP(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/storage_KT19jP.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/storage_KT19jP.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_storage_KT19jP(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/storage_KT19jP.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_op6Jjx(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_op6Jjx.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_op6Jjx.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_op6Jjx(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_op6Jjx.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_op6Jjx.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_op6Jjx(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_op6Jjx.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_onrsfd(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_onrsfd.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_onrsfd.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_onrsfd(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_onrsfd.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_onrsfd.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_onrsfd(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_onrsfd.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_onnVBH(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_onnVBH.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_onnVBH.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_onnVBH(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_onnVBH.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_onnVBH.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_onnVBH(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_onnVBH.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_opQjjr(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_opQjjr.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_opQjjr.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_opQjjr(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_opQjjr.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_opQjjr.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_opQjjr(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_opQjjr.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_ooaW9j(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_ooaW9j.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_ooaW9j.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_ooaW9j(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_ooaW9j.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_ooaW9j.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_ooaW9j(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_ooaW9j.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_onnBLb(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_onnBLb.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_onnBLb.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_onnBLb(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_onnBLb.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_onnBLb.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_onnBLb(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_onnBLb.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_ooJ3VU(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_ooJ3VU.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_ooJ3VU.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_ooJ3VU(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_ooJ3VU.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_ooJ3VU.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_ooJ3VU(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_ooJ3VU.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_op8Bbm(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_op8Bbm.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_op8Bbm.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_op8Bbm(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_op8Bbm.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_op8Bbm.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_op8Bbm(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_op8Bbm.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_oohuCM(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_oohuCM.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_oohuCM.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_oohuCM(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_oohuCM.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_oohuCM.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_oohuCM(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_oohuCM.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_ooMXxF(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_ooMXxF.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_ooMXxF.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_ooMXxF(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_ooMXxF.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_ooMXxF.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_ooMXxF(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT19jPpyfiiS66AsNmcytmHtKwTnfsBe6XSK/parameter_ooMXxF.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)
