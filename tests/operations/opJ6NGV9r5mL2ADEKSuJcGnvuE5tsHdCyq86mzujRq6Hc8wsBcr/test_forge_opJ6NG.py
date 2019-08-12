from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopJ6NG(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opJ6NG(self):
        expected = get_data(
            path='operations/opJ6NGV9r5mL2ADEKSuJcGnvuE5tsHdCyq86mzujRq6Hc8wsBcr/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opJ6NGV9r5mL2ADEKSuJcGnvuE5tsHdCyq86mzujRq6Hc8wsBcr/unsigned.json'))
        self.assertEqual(expected, actual)
