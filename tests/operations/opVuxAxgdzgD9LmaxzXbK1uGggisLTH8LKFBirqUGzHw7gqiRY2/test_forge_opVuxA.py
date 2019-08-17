from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopVuxA(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opVuxA(self):
        expected = get_data(
            path='operations/opVuxAxgdzgD9LmaxzXbK1uGggisLTH8LKFBirqUGzHw7gqiRY2/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opVuxAxgdzgD9LmaxzXbK1uGggisLTH8LKFBirqUGzHw7gqiRY2/unsigned.json'))
        self.assertEqual(expected, actual)
