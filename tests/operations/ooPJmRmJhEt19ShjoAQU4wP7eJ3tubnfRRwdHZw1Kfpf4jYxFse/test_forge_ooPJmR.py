from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooPJmR(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooPJmR(self):
        expected = get_data(
            path='operations/ooPJmRmJhEt19ShjoAQU4wP7eJ3tubnfRRwdHZw1Kfpf4jYxFse/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooPJmRmJhEt19ShjoAQU4wP7eJ3tubnfRRwdHZw1Kfpf4jYxFse/unsigned.json'))
        self.assertEqual(expected, actual)
