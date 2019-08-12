from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooQ1z5(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooQ1z5(self):
        expected = get_data(
            path='operations/ooQ1z5D1qjud5rKcDdHV4XeYQHuHd3WhxRYS74HywMKYmeehQ8M/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooQ1z5D1qjud5rKcDdHV4XeYQHuHd3WhxRYS74HywMKYmeehQ8M/unsigned.json'))
        self.assertEqual(expected, actual)
