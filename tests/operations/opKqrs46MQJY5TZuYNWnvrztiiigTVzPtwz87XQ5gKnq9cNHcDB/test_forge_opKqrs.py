from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopKqrs(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opKqrs(self):
        expected = get_data(
            path='operations/opKqrs46MQJY5TZuYNWnvrztiiigTVzPtwz87XQ5gKnq9cNHcDB/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opKqrs46MQJY5TZuYNWnvrztiiigTVzPtwz87XQ5gKnq9cNHcDB/unsigned.json'))
        self.assertEqual(expected, actual)
