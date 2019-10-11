from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopRcji(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opRcji(self):
        expected = get_data(
            path='operations/opRcjiXMSS6L9F36AVCzF2b4tG3HuJRkMVQ8Y8ynGm6MrC5HWue/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opRcjiXMSS6L9F36AVCzF2b4tG3HuJRkMVQ8Y8ynGm6MrC5HWue/unsigned.json'))
        self.assertEqual(expected, actual)
