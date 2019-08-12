from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopaT8j(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opaT8j(self):
        expected = get_data(
            path='operations/opaT8joci6STzhKpCPFmSyBjyxpAhzMgX78RVP4uPaoVjAFTFB9/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opaT8joci6STzhKpCPFmSyBjyxpAhzMgX78RVP4uPaoVjAFTFB9/unsigned.json'))
        self.assertEqual(expected, actual)
