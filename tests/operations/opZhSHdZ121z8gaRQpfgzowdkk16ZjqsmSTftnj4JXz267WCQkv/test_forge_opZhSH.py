from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopZhSH(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opZhSH(self):
        expected = get_data(
            path='operations/opZhSHdZ121z8gaRQpfgzowdkk16ZjqsmSTftnj4JXz267WCQkv/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opZhSHdZ121z8gaRQpfgzowdkk16ZjqsmSTftnj4JXz267WCQkv/unsigned.json'))
        self.assertEqual(expected, actual)
