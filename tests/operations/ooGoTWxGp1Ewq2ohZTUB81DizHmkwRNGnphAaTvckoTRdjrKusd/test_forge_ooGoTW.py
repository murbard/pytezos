from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooGoTW(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooGoTW(self):
        expected = get_data(
            path='operations/ooGoTWxGp1Ewq2ohZTUB81DizHmkwRNGnphAaTvckoTRdjrKusd/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooGoTWxGp1Ewq2ohZTUB81DizHmkwRNGnphAaTvckoTRdjrKusd/unsigned.json'))
        self.assertEqual(expected, actual)
