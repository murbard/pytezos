from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopKXNN(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opKXNN(self):
        expected = get_data(
            path='operations/opKXNNo59NM6WepUEX5nYv5BvirAJq3f9ZZSMzzqropEWki17Ay/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opKXNNo59NM6WepUEX5nYv5BvirAJq3f9ZZSMzzqropEWki17Ay/unsigned.json'))
        self.assertEqual(expected, actual)
