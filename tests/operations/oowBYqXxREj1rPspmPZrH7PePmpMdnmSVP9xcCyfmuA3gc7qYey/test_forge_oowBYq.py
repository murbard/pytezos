from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoowBYq(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oowBYq(self):
        expected = get_data(
            path='operations/oowBYqXxREj1rPspmPZrH7PePmpMdnmSVP9xcCyfmuA3gc7qYey/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oowBYqXxREj1rPspmPZrH7PePmpMdnmSVP9xcCyfmuA3gc7qYey/unsigned.json'))
        self.assertEqual(expected, actual)
