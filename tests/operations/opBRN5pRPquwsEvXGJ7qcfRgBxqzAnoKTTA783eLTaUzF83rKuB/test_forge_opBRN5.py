from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopBRN5(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opBRN5(self):
        expected = get_data(
            path='operations/opBRN5pRPquwsEvXGJ7qcfRgBxqzAnoKTTA783eLTaUzF83rKuB/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opBRN5pRPquwsEvXGJ7qcfRgBxqzAnoKTTA783eLTaUzF83rKuB/unsigned.json'))
        self.assertEqual(expected, actual)
