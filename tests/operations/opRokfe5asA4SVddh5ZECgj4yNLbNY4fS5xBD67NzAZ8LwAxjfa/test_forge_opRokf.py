from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopRokf(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opRokf(self):
        expected = get_data(
            path='operations/opRokfe5asA4SVddh5ZECgj4yNLbNY4fS5xBD67NzAZ8LwAxjfa/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opRokfe5asA4SVddh5ZECgj4yNLbNY4fS5xBD67NzAZ8LwAxjfa/unsigned.json'))
        self.assertEqual(expected, actual)
