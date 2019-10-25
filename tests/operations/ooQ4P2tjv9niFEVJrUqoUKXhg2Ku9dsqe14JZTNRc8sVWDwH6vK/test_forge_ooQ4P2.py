from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooQ4P2(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooQ4P2(self):
        expected = get_data(
            path='operations/ooQ4P2tjv9niFEVJrUqoUKXhg2Ku9dsqe14JZTNRc8sVWDwH6vK/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooQ4P2tjv9niFEVJrUqoUKXhg2Ku9dsqe14JZTNRc8sVWDwH6vK/unsigned.json'))
        self.assertEqual(expected, actual)
