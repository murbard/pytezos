from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopF2eT(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opF2eT(self):
        expected = get_data(
            path='operations/opF2eTQCuCouNpuRBhdJnwaKVAveUAZLUN8bWGhn7fPqHqJMrmG/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opF2eTQCuCouNpuRBhdJnwaKVAveUAZLUN8bWGhn7fPqHqJMrmG/unsigned.json'))
        self.assertEqual(expected, actual)
