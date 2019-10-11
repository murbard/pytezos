from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooweht(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooweht(self):
        expected = get_data(
            path='operations/oowehtRB5Zz8YKyQwNH4NK1Y2K1X6gzPFj7ZFXkriB6Smeu7SqC/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oowehtRB5Zz8YKyQwNH4NK1Y2K1X6gzPFj7ZFXkriB6Smeu7SqC/unsigned.json'))
        self.assertEqual(expected, actual)
