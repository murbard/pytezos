from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoofJnm(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oofJnm(self):
        expected = get_data(
            path='operations/oofJnmcfXUnHW7FdSn4zE3XrQzma6bWCJBwTVmjKKKcrWV715Yi/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oofJnmcfXUnHW7FdSn4zE3XrQzma6bWCJBwTVmjKKKcrWV715Yi/unsigned.json'))
        self.assertEqual(expected, actual)
