from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonghtm(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onghtm(self):
        expected = get_data(
            path='operations/onghtmJHXVPdyxt5HGGqmXXmcwkeQVX4uPh3akEsdFbTKe3n9Ba/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onghtmJHXVPdyxt5HGGqmXXmcwkeQVX4uPh3akEsdFbTKe3n9Ba/unsigned.json'))
        self.assertEqual(expected, actual)
