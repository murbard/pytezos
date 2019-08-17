from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooJJkW(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooJJkW(self):
        expected = get_data(
            path='operations/ooJJkWFNWtrd9TAJm6D3tcBNJbWKAXbc1ZzB1J1uoAYvF4DztY5/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooJJkWFNWtrd9TAJm6D3tcBNJbWKAXbc1ZzB1J1uoAYvF4DztY5/unsigned.json'))
        self.assertEqual(expected, actual)
