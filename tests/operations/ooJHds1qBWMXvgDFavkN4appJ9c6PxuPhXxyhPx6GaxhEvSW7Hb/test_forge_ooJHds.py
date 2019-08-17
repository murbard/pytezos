from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooJHds(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooJHds(self):
        expected = get_data(
            path='operations/ooJHds1qBWMXvgDFavkN4appJ9c6PxuPhXxyhPx6GaxhEvSW7Hb/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooJHds1qBWMXvgDFavkN4appJ9c6PxuPhXxyhPx6GaxhEvSW7Hb/unsigned.json'))
        self.assertEqual(expected, actual)
