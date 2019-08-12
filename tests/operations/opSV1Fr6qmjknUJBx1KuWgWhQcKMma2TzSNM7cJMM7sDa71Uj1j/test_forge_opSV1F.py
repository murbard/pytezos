from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopSV1F(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opSV1F(self):
        expected = get_data(
            path='operations/opSV1Fr6qmjknUJBx1KuWgWhQcKMma2TzSNM7cJMM7sDa71Uj1j/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opSV1Fr6qmjknUJBx1KuWgWhQcKMma2TzSNM7cJMM7sDa71Uj1j/unsigned.json'))
        self.assertEqual(expected, actual)
