from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooq5un(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooq5un(self):
        expected = get_data(
            path='operations/ooq5uncwE23zji3XEDobFa21BwooDYBv7DDz3A4LBVAep1hNprx/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooq5uncwE23zji3XEDobFa21BwooDYBv7DDz3A4LBVAep1hNprx/unsigned.json'))
        self.assertEqual(expected, actual)
