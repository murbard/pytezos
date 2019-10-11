from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoodLWy(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oodLWy(self):
        expected = get_data(
            path='operations/oodLWyjjJtMA4rNQoHFycUS5dqx6prXPqepFfak96hgnk8K15Dj/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oodLWyjjJtMA4rNQoHFycUS5dqx6prXPqepFfak96hgnk8K15Dj/unsigned.json'))
        self.assertEqual(expected, actual)
