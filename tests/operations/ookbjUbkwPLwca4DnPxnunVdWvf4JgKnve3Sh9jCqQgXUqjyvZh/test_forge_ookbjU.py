from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestookbjU(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ookbjU(self):
        expected = get_data(
            path='operations/ookbjUbkwPLwca4DnPxnunVdWvf4JgKnve3Sh9jCqQgXUqjyvZh/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ookbjUbkwPLwca4DnPxnunVdWvf4JgKnve3Sh9jCqQgXUqjyvZh/unsigned.json'))
        self.assertEqual(expected, actual)
