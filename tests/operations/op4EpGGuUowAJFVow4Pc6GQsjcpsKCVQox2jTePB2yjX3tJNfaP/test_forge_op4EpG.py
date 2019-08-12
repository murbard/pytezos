from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop4EpG(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op4EpG(self):
        expected = get_data(
            path='operations/op4EpGGuUowAJFVow4Pc6GQsjcpsKCVQox2jTePB2yjX3tJNfaP/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op4EpGGuUowAJFVow4Pc6GQsjcpsKCVQox2jTePB2yjX3tJNfaP/unsigned.json'))
        self.assertEqual(expected, actual)
