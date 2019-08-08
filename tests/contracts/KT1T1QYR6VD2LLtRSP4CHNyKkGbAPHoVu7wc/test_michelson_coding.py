from unittest import TestCase

from tests import get_data
from pytezos.michelson.coding import micheline_to_michelson, michelson_to_micheline


class MichelsonCodingTestKT1T1Q(TestCase):
    
    def setUp(self):
        self.maxDiff = None

    def test_michelson_parse_code_KT1T1Q(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/code_KT1T1Q.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/code_KT1T1Q.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_code_KT1T1Q(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/code_KT1T1Q.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/code_KT1T1Q.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_code_KT1T1Q(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/code_KT1T1Q.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_storage_KT1T1Q(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/storage_KT1T1Q.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/storage_KT1T1Q.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_storage_KT1T1Q(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/storage_KT1T1Q.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/storage_KT1T1Q.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_storage_KT1T1Q(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/storage_KT1T1Q.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_opDY37(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_opDY37.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_opDY37.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_opDY37(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_opDY37.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_opDY37.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_opDY37(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_opDY37.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_ooFVFm(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_ooFVFm.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_ooFVFm.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_ooFVFm(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_ooFVFm.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_ooFVFm.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_ooFVFm(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_ooFVFm.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_op3JH8(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_op3JH8.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_op3JH8.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_op3JH8(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_op3JH8.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_op3JH8.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_op3JH8(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_op3JH8.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_opJuDD(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_opJuDD.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_opJuDD.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_opJuDD(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_opJuDD.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_opJuDD.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_opJuDD(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_opJuDD.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_op9fva(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_op9fva.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_op9fva.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_op9fva(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_op9fva.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_op9fva.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_op9fva(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_op9fva.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_op6G8U(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_op6G8U.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_op6G8U.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_op6G8U(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_op6G8U.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_op6G8U.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_op6G8U(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_op6G8U.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_onmrnk(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_onmrnk.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_onmrnk.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_onmrnk(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_onmrnk.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_onmrnk.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_onmrnk(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_onmrnk.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_onhhuc(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_onhhuc.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_onhhuc.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_onhhuc(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_onhhuc.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_onhhuc.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_onhhuc(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_onhhuc.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_ookNta(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_ookNta.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_ookNta.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_ookNta(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_ookNta.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_ookNta.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_ookNta(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_ookNta.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)

    def test_michelson_parse_parameter_ooynpY(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_ooynpY.json')
        actual = michelson_to_micheline(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_ooynpY.tz'))
        self.assertEqual(expected, actual)

    def test_michelson_format_parameter_ooynpY(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_ooynpY.tz')
        actual = micheline_to_michelson(get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_ooynpY.json'), 
            inline=True)
        self.assertEqual(expected, actual)

    def test_michelson_inverse_parameter_ooynpY(self):
        expected = get_data(
            path='/home/mickey/pytezos/tests/contracts/KT1T1QYR6VD2LLtRSP4CHNyKkGbAPHoVu7wc/parameter_ooynpY.json')
        actual = michelson_to_micheline(micheline_to_michelson(expected))
        self.assertEqual(expected, actual)
