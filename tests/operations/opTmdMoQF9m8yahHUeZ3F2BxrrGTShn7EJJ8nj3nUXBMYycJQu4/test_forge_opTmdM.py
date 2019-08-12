from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopTmdM(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opTmdM(self):
        expected = get_data(
            path='operations/opTmdMoQF9m8yahHUeZ3F2BxrrGTShn7EJJ8nj3nUXBMYycJQu4/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opTmdMoQF9m8yahHUeZ3F2BxrrGTShn7EJJ8nj3nUXBMYycJQu4/unsigned.json'))
        self.assertEqual(expected, actual)
