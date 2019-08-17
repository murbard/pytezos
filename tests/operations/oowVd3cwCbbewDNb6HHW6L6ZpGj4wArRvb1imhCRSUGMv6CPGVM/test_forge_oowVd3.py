from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoowVd3(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oowVd3(self):
        expected = get_data(
            path='operations/oowVd3cwCbbewDNb6HHW6L6ZpGj4wArRvb1imhCRSUGMv6CPGVM/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oowVd3cwCbbewDNb6HHW6L6ZpGj4wArRvb1imhCRSUGMv6CPGVM/unsigned.json'))
        self.assertEqual(expected, actual)
