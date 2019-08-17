from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonspRK(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onspRK(self):
        expected = get_data(
            path='operations/onspRK5EkzY1xjGrg8h1WEhAMmuoLoTG7NS1HUHG2ek6qusPWQg/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onspRK5EkzY1xjGrg8h1WEhAMmuoLoTG7NS1HUHG2ek6qusPWQg/unsigned.json'))
        self.assertEqual(expected, actual)
