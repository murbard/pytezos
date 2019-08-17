from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooG9Ft(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooG9Ft(self):
        expected = get_data(
            path='operations/ooG9Fttc2Fq3MJctnM8WjUwNLzazD8Y5kTqW3hMoeN5qWykFfKT/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooG9Fttc2Fq3MJctnM8WjUwNLzazD8Y5kTqW3hMoeN5qWykFfKT/unsigned.json'))
        self.assertEqual(expected, actual)
