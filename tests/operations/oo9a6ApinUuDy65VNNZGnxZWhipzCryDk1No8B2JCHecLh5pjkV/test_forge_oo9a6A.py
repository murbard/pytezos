from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo9a6A(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo9a6A(self):
        expected = get_data(
            path='operations/oo9a6ApinUuDy65VNNZGnxZWhipzCryDk1No8B2JCHecLh5pjkV/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo9a6ApinUuDy65VNNZGnxZWhipzCryDk1No8B2JCHecLh5pjkV/unsigned.json'))
        self.assertEqual(expected, actual)
