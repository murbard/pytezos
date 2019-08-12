from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooSu8z(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooSu8z(self):
        expected = get_data(
            path='operations/ooSu8zt5TDrHKGTExz2JwH7UiVZ8R53LdGvugdfajV9VE38mk5x/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooSu8zt5TDrHKGTExz2JwH7UiVZ8R53LdGvugdfajV9VE38mk5x/unsigned.json'))
        self.assertEqual(expected, actual)
