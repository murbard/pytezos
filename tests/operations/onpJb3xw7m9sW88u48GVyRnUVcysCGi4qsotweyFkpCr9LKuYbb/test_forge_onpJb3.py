from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonpJb3(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onpJb3(self):
        expected = get_data(
            path='operations/onpJb3xw7m9sW88u48GVyRnUVcysCGi4qsotweyFkpCr9LKuYbb/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onpJb3xw7m9sW88u48GVyRnUVcysCGi4qsotweyFkpCr9LKuYbb/unsigned.json'))
        self.assertEqual(expected, actual)
