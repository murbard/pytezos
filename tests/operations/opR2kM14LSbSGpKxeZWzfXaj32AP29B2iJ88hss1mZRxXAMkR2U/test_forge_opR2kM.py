from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopR2kM(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opR2kM(self):
        expected = get_data(
            path='operations/opR2kM14LSbSGpKxeZWzfXaj32AP29B2iJ88hss1mZRxXAMkR2U/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opR2kM14LSbSGpKxeZWzfXaj32AP29B2iJ88hss1mZRxXAMkR2U/unsigned.json'))
        self.assertEqual(expected, actual)
