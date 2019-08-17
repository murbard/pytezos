from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoob72p(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oob72p(self):
        expected = get_data(
            path='operations/oob72p1eGaAx94gE7GCUFit3B89jukZkniqRi6ndYgU2zm7LxYt/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oob72p1eGaAx94gE7GCUFit3B89jukZkniqRi6ndYgU2zm7LxYt/unsigned.json'))
        self.assertEqual(expected, actual)
