from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo2Exc(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo2Exc(self):
        expected = get_data(
            path='operations/oo2ExcPsAT4otdE7WftZkUuVapZxaSTogbJfPkRuJBjwYtRTk8f/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo2ExcPsAT4otdE7WftZkUuVapZxaSTogbJfPkRuJBjwYtRTk8f/unsigned.json'))
        self.assertEqual(expected, actual)
