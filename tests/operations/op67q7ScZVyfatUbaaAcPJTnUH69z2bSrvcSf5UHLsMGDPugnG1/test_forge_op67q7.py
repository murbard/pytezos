from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop67q7(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op67q7(self):
        expected = get_data(
            path='operations/op67q7ScZVyfatUbaaAcPJTnUH69z2bSrvcSf5UHLsMGDPugnG1/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op67q7ScZVyfatUbaaAcPJTnUH69z2bSrvcSf5UHLsMGDPugnG1/unsigned.json'))
        self.assertEqual(expected, actual)
