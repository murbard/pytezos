from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooSwCB(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooSwCB(self):
        expected = get_data(
            path='operations/ooSwCBx8o7v6i6hZanXdbvNm72zksk9hpfd41RwnpmXz5yjsfQj/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooSwCBx8o7v6i6hZanXdbvNm72zksk9hpfd41RwnpmXz5yjsfQj/unsigned.json'))
        self.assertEqual(expected, actual)
