from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooncCo(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooncCo(self):
        expected = get_data(
            path='operations/ooncCooi3fkTAWXEdCtk8paHry4xMfokfgRvJkwTSdoe5MbuGVx/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooncCooi3fkTAWXEdCtk8paHry4xMfokfgRvJkwTSdoe5MbuGVx/unsigned.json'))
        self.assertEqual(expected, actual)
