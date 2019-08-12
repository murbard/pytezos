from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoos7Ad(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oos7Ad(self):
        expected = get_data(
            path='operations/oos7Adk8JsX8sh2JLz921VKigAza5XAWAaLhNboCm4NHnveD5Q4/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oos7Adk8JsX8sh2JLz921VKigAza5XAWAaLhNboCm4NHnveD5Q4/unsigned.json'))
        self.assertEqual(expected, actual)
