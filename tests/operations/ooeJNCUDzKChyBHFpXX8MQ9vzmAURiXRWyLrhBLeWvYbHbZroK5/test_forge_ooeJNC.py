from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooeJNC(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooeJNC(self):
        expected = get_data(
            path='operations/ooeJNCUDzKChyBHFpXX8MQ9vzmAURiXRWyLrhBLeWvYbHbZroK5/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooeJNCUDzKChyBHFpXX8MQ9vzmAURiXRWyLrhBLeWvYbHbZroK5/unsigned.json'))
        self.assertEqual(expected, actual)
