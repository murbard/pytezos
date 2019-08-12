from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopaknQ(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opaknQ(self):
        expected = get_data(
            path='operations/opaknQzCq1JhzjAUTbUNQbKxpTGYPPCHpqLtpp19pDUGsoexr5J/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opaknQzCq1JhzjAUTbUNQbKxpTGYPPCHpqLtpp19pDUGsoexr5J/unsigned.json'))
        self.assertEqual(expected, actual)
