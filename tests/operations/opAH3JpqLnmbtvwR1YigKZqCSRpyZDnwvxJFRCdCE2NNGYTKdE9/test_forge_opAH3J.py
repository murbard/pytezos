from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopAH3J(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opAH3J(self):
        expected = get_data(
            path='operations/opAH3JpqLnmbtvwR1YigKZqCSRpyZDnwvxJFRCdCE2NNGYTKdE9/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opAH3JpqLnmbtvwR1YigKZqCSRpyZDnwvxJFRCdCE2NNGYTKdE9/unsigned.json'))
        self.assertEqual(expected, actual)
