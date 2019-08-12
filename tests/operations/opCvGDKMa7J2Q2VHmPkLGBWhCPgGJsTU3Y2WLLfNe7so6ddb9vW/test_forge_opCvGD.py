from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopCvGD(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opCvGD(self):
        expected = get_data(
            path='operations/opCvGDKMa7J2Q2VHmPkLGBWhCPgGJsTU3Y2WLLfNe7so6ddb9vW/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opCvGDKMa7J2Q2VHmPkLGBWhCPgGJsTU3Y2WLLfNe7so6ddb9vW/unsigned.json'))
        self.assertEqual(expected, actual)
