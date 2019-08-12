from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooXjrj(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooXjrj(self):
        expected = get_data(
            path='operations/ooXjrjy5DmGZAfz5wp6VmvtPrWEkXvQXT76NdhXe3GMrpvzqZcc/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooXjrjy5DmGZAfz5wp6VmvtPrWEkXvQXT76NdhXe3GMrpvzqZcc/unsigned.json'))
        self.assertEqual(expected, actual)
