from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestony6Hg(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ony6Hg(self):
        expected = get_data(
            path='operations/ony6Hgd7uqmyLx8hLL7i8B2NUUxp4MbdeBXNXTT3VFSodXcCwAH/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ony6Hgd7uqmyLx8hLL7i8B2NUUxp4MbdeBXNXTT3VFSodXcCwAH/unsigned.json'))
        self.assertEqual(expected, actual)
