from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooXZtx(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooXZtx(self):
        expected = get_data(
            path='operations/ooXZtxQB41UqWFMthZ52mRnuEDN4xGBuw4M6YjsDmvtiXfeng5p/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooXZtxQB41UqWFMthZ52mRnuEDN4xGBuw4M6YjsDmvtiXfeng5p/unsigned.json'))
        self.assertEqual(expected, actual)
