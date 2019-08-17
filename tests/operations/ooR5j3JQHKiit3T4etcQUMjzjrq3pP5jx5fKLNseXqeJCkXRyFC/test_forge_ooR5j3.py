from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooR5j3(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooR5j3(self):
        expected = get_data(
            path='operations/ooR5j3JQHKiit3T4etcQUMjzjrq3pP5jx5fKLNseXqeJCkXRyFC/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooR5j3JQHKiit3T4etcQUMjzjrq3pP5jx5fKLNseXqeJCkXRyFC/unsigned.json'))
        self.assertEqual(expected, actual)
