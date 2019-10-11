from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoohafK(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oohafK(self):
        expected = get_data(
            path='operations/oohafKVbkS3Xv98MN9js66nnM1aWgfaKGfsEaMgmNQfyPSJ7pfN/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oohafKVbkS3Xv98MN9js66nnM1aWgfaKGfsEaMgmNQfyPSJ7pfN/unsigned.json'))
        self.assertEqual(expected, actual)
