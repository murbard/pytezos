from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo1rPf(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo1rPf(self):
        expected = get_data(
            path='operations/oo1rPfLWEAJhqkifMpnApdSGJjWmQF95ruxgP1kTQkUnr5dSvvH/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo1rPfLWEAJhqkifMpnApdSGJjWmQF95ruxgP1kTQkUnr5dSvvH/unsigned.json'))
        self.assertEqual(expected, actual)
