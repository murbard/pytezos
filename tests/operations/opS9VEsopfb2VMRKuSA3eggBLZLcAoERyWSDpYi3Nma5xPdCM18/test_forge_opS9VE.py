from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopS9VE(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opS9VE(self):
        expected = get_data(
            path='operations/opS9VEsopfb2VMRKuSA3eggBLZLcAoERyWSDpYi3Nma5xPdCM18/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opS9VEsopfb2VMRKuSA3eggBLZLcAoERyWSDpYi3Nma5xPdCM18/unsigned.json'))
        self.assertEqual(expected, actual)
