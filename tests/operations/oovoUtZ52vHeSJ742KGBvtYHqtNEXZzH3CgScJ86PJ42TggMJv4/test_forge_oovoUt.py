from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoovoUt(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oovoUt(self):
        expected = get_data(
            path='operations/oovoUtZ52vHeSJ742KGBvtYHqtNEXZzH3CgScJ86PJ42TggMJv4/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oovoUtZ52vHeSJ742KGBvtYHqtNEXZzH3CgScJ86PJ42TggMJv4/unsigned.json'))
        self.assertEqual(expected, actual)
