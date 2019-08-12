from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo2DJ5(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo2DJ5(self):
        expected = get_data(
            path='operations/oo2DJ5Sgj3WmHcxPLjzcJfrXECZFjuohs2PgegXT8vJfdFWss5h/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo2DJ5Sgj3WmHcxPLjzcJfrXECZFjuohs2PgegXT8vJfdFWss5h/unsigned.json'))
        self.assertEqual(expected, actual)
