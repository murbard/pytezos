from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoow5i2(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oow5i2(self):
        expected = get_data(
            path='operations/oow5i2vAiDNYrWR8tYo7DomgFtGF7AZaJ8Sn845UoDBE2bhe4EQ/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oow5i2vAiDNYrWR8tYo7DomgFtGF7AZaJ8Sn845UoDBE2bhe4EQ/unsigned.json'))
        self.assertEqual(expected, actual)
