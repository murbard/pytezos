from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonqe9E(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onqe9E(self):
        expected = get_data(
            path='operations/onqe9Ebf5j3d4dQ2TRXjBhT4HgDCVu1w8grXdz2YTgdcZbY8DuR/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onqe9Ebf5j3d4dQ2TRXjBhT4HgDCVu1w8grXdz2YTgdcZbY8DuR/unsigned.json'))
        self.assertEqual(expected, actual)
