from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopTSMD(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opTSMD(self):
        expected = get_data(
            path='operations/opTSMDn64MFD8grXxzpmTui8w7JZNE4m99XMEaARkzov4Fkm67h/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opTSMDn64MFD8grXxzpmTui8w7JZNE4m99XMEaARkzov4Fkm67h/unsigned.json'))
        self.assertEqual(expected, actual)
