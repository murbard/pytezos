from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooGC7N(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooGC7N(self):
        expected = get_data(
            path='operations/ooGC7NoTs7bsbzJSWchZv5Ut53rf5Vqu3nHDgztDdmGMn5MHHup/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooGC7NoTs7bsbzJSWchZv5Ut53rf5Vqu3nHDgztDdmGMn5MHHup/unsigned.json'))
        self.assertEqual(expected, actual)
