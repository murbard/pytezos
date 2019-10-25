from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo3NCV(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo3NCV(self):
        expected = get_data(
            path='operations/oo3NCVnFCPuEncM9oM5gp7RqtJSzheJbEzox6ozVnFLiwwZ4vkA/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo3NCVnFCPuEncM9oM5gp7RqtJSzheJbEzox6ozVnFLiwwZ4vkA/unsigned.json'))
        self.assertEqual(expected, actual)
