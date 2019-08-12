from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonvhYW(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onvhYW(self):
        expected = get_data(
            path='operations/onvhYWosSt6x5kHd9FbE9hb8UxXdC3qPZanAVvUPGtv5XgE8cux/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onvhYWosSt6x5kHd9FbE9hb8UxXdC3qPZanAVvUPGtv5XgE8cux/unsigned.json'))
        self.assertEqual(expected, actual)
