from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonr27f(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onr27f(self):
        expected = get_data(
            path='operations/onr27fqraujYQDYayYZhi9uDfFBJyZnHKkHFn4oQyLSfQ97sc7m/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onr27fqraujYQDYayYZhi9uDfFBJyZnHKkHFn4oQyLSfQ97sc7m/unsigned.json'))
        self.assertEqual(expected, actual)
