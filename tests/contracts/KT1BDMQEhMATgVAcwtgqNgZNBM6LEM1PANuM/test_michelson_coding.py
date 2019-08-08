from unittest import TestCase
import json

from tests import get_data
from pytezos.michelson.coding import micheline_to_michelson, michelson_to_micheline


class MichelsonCodingTestKT1BDM(TestCase):
    
    def setUp(self):
        self.maxDiff = None

    def test_michelson_parse_code_KT1BDM(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/code_KT1BDM.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/code_KT1BDM.tz'))
        e = json.dumps(expected, indent=2, sort_keys=True)
        a = json.dumps(actual, indent=2, sort_keys=True)
        self.assertEqual(e, a)

    def test_michelson_format_code_KT1BDM(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/code_KT1BDM.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/code_KT1BDM.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_code_KT1BDM(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/code_KT1BDM.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_storage_KT1BDM(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/storage_KT1BDM.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/storage_KT1BDM.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_storage_KT1BDM(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/storage_KT1BDM.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/storage_KT1BDM.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_storage_KT1BDM(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/storage_KT1BDM.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_ooMDoN(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooMDoN.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooMDoN.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_ooMDoN(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooMDoN.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooMDoN.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_ooMDoN(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooMDoN.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_ooT7Uy(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooT7Uy.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooT7Uy.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_ooT7Uy(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooT7Uy.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooT7Uy.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_ooT7Uy(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooT7Uy.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_onuB3S(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_onuB3S.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_onuB3S.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_onuB3S(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_onuB3S.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_onuB3S.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_onuB3S(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_onuB3S.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_ooArSr(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooArSr.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooArSr.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_ooArSr(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooArSr.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooArSr.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_ooArSr(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooArSr.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_onrCFo(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_onrCFo.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_onrCFo.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_onrCFo(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_onrCFo.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_onrCFo.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_onrCFo(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_onrCFo.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_ongBCW(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ongBCW.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ongBCW.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_ongBCW(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ongBCW.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ongBCW.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_ongBCW(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ongBCW.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_ooe4gB(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooe4gB.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooe4gB.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_ooe4gB(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooe4gB.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooe4gB.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_ooe4gB(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooe4gB.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_onkisK(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_onkisK.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_onkisK.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_onkisK(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_onkisK.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_onkisK.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_onkisK(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_onkisK.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_oodaaD(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_oodaaD.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_oodaaD.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_oodaaD(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_oodaaD.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_oodaaD.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_oodaaD(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_oodaaD.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_ooRvV7(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooRvV7.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooRvV7.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_ooRvV7(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooRvV7.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooRvV7.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_ooRvV7(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1BDMQEhMATgVAcwtgqNgZNBM6LEM1PANuM/parameter_ooRvV7.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)
