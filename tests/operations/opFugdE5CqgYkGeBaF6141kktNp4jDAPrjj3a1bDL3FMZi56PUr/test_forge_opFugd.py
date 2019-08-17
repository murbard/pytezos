from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopFugd(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opFugd(self):
        expected = get_data(
            path='operations/opFugdE5CqgYkGeBaF6141kktNp4jDAPrjj3a1bDL3FMZi56PUr/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opFugdE5CqgYkGeBaF6141kktNp4jDAPrjj3a1bDL3FMZi56PUr/unsigned.json'))
        self.assertEqual(expected, actual)
