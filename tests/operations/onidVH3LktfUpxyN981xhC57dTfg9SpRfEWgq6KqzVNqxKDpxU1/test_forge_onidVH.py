from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonidVH(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onidVH(self):
        expected = get_data(
            path='operations/onidVH3LktfUpxyN981xhC57dTfg9SpRfEWgq6KqzVNqxKDpxU1/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onidVH3LktfUpxyN981xhC57dTfg9SpRfEWgq6KqzVNqxKDpxU1/unsigned.json'))
        self.assertEqual(expected, actual)
