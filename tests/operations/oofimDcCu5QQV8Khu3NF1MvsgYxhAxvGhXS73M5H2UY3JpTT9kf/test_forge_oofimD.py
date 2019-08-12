from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoofimD(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oofimD(self):
        expected = get_data(
            path='operations/oofimDcCu5QQV8Khu3NF1MvsgYxhAxvGhXS73M5H2UY3JpTT9kf/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oofimDcCu5QQV8Khu3NF1MvsgYxhAxvGhXS73M5H2UY3JpTT9kf/unsigned.json'))
        self.assertEqual(expected, actual)
