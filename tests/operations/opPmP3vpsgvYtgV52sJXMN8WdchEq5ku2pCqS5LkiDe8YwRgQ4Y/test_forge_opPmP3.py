from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopPmP3(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opPmP3(self):
        expected = get_data(
            path='operations/opPmP3vpsgvYtgV52sJXMN8WdchEq5ku2pCqS5LkiDe8YwRgQ4Y/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opPmP3vpsgvYtgV52sJXMN8WdchEq5ku2pCqS5LkiDe8YwRgQ4Y/unsigned.json'))
        self.assertEqual(expected, actual)
