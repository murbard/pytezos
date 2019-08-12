from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonxdSA(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onxdSA(self):
        expected = get_data(
            path='operations/onxdSAawYuoDcroSa7mEHMhzWHMJe11c3WPprF6KQtpLb9Dmt8V/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onxdSAawYuoDcroSa7mEHMhzWHMJe11c3WPprF6KQtpLb9Dmt8V/unsigned.json'))
        self.assertEqual(expected, actual)
