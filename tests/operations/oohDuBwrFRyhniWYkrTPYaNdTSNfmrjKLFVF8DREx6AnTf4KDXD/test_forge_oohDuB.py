from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoohDuB(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oohDuB(self):
        expected = get_data(
            path='operations/oohDuBwrFRyhniWYkrTPYaNdTSNfmrjKLFVF8DREx6AnTf4KDXD/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oohDuBwrFRyhniWYkrTPYaNdTSNfmrjKLFVF8DREx6AnTf4KDXD/unsigned.json'))
        self.assertEqual(expected, actual)
