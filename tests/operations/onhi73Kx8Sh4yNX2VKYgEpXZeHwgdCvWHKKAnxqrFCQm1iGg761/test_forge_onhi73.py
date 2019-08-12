from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonhi73(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onhi73(self):
        expected = get_data(
            path='operations/onhi73Kx8Sh4yNX2VKYgEpXZeHwgdCvWHKKAnxqrFCQm1iGg761/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onhi73Kx8Sh4yNX2VKYgEpXZeHwgdCvWHKKAnxqrFCQm1iGg761/unsigned.json'))
        self.assertEqual(expected, actual)
