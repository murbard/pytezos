from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop4x91(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op4x91(self):
        expected = get_data(
            path='operations/op4x91eahsbqdPaPpAR9upQVkai1GF46geV4btkak5rBNwJDC4j/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op4x91eahsbqdPaPpAR9upQVkai1GF46geV4btkak5rBNwJDC4j/unsigned.json'))
        self.assertEqual(expected, actual)
