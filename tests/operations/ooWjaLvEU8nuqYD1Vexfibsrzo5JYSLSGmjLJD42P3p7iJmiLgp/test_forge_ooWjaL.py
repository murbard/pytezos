from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooWjaL(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooWjaL(self):
        expected = get_data(
            path='operations/ooWjaLvEU8nuqYD1Vexfibsrzo5JYSLSGmjLJD42P3p7iJmiLgp/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooWjaLvEU8nuqYD1Vexfibsrzo5JYSLSGmjLJD42P3p7iJmiLgp/unsigned.json'))
        self.assertEqual(expected, actual)
