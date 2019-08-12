from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopV2C4(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opV2C4(self):
        expected = get_data(
            path='operations/opV2C4panQKSb5bmesjVuZ94RAqhQSzThZcoYiiWajnfz442FE6/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opV2C4panQKSb5bmesjVuZ94RAqhQSzThZcoYiiWajnfz442FE6/unsigned.json'))
        self.assertEqual(expected, actual)
