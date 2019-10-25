from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopMAPy(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opMAPy(self):
        expected = get_data(
            path='operations/opMAPyzaCAcW37kFfLcUg3MgNbkG27wSBafJcubqMuii5Ur7EZj/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opMAPyzaCAcW37kFfLcUg3MgNbkG27wSBafJcubqMuii5Ur7EZj/unsigned.json'))
        self.assertEqual(expected, actual)
