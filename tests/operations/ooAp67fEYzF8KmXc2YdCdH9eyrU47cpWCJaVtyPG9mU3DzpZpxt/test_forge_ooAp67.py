from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooAp67(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooAp67(self):
        expected = get_data(
            path='operations/ooAp67fEYzF8KmXc2YdCdH9eyrU47cpWCJaVtyPG9mU3DzpZpxt/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooAp67fEYzF8KmXc2YdCdH9eyrU47cpWCJaVtyPG9mU3DzpZpxt/unsigned.json'))
        self.assertEqual(expected, actual)
