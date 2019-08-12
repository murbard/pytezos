from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopFHtM(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opFHtM(self):
        expected = get_data(
            path='operations/opFHtMcRRDoB7Puafue2Gexaaph8TndYKKJzT49vYUvTuZbcMNQ/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opFHtMcRRDoB7Puafue2Gexaaph8TndYKKJzT49vYUvTuZbcMNQ/unsigned.json'))
        self.assertEqual(expected, actual)
