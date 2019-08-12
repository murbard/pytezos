from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoooCi8(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oooCi8(self):
        expected = get_data(
            path='operations/oooCi8ftQji7qPGdJMStoepCA2rbby5nosnymhtu6j3DX7c3R8X/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oooCi8ftQji7qPGdJMStoepCA2rbby5nosnymhtu6j3DX7c3R8X/unsigned.json'))
        self.assertEqual(expected, actual)
