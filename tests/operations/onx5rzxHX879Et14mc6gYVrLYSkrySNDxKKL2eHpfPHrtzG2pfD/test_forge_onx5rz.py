from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonx5rz(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onx5rz(self):
        expected = get_data(
            path='operations/onx5rzxHX879Et14mc6gYVrLYSkrySNDxKKL2eHpfPHrtzG2pfD/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onx5rzxHX879Et14mc6gYVrLYSkrySNDxKKL2eHpfPHrtzG2pfD/unsigned.json'))
        self.assertEqual(expected, actual)
