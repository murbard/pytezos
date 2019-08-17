from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopYx73(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opYx73(self):
        expected = get_data(
            path='operations/opYx73KiUVkhhj9RPr92ntVhm9cAmurbrU6MghAqNHEJk1VgYUJ/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opYx73KiUVkhhj9RPr92ntVhm9cAmurbrU6MghAqNHEJk1VgYUJ/unsigned.json'))
        self.assertEqual(expected, actual)
