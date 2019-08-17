from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooGhDP(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooGhDP(self):
        expected = get_data(
            path='operations/ooGhDP2eFiDTKF6bEsGjdYkz7cJty8X3PeTm6xLsVttvD4Qz1ZD/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooGhDP2eFiDTKF6bEsGjdYkz7cJty8X3PeTm6xLsVttvD4Qz1ZD/unsigned.json'))
        self.assertEqual(expected, actual)
