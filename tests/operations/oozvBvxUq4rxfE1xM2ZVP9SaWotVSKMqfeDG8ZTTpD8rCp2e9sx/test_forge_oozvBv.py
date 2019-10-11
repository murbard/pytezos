from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoozvBv(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oozvBv(self):
        expected = get_data(
            path='operations/oozvBvxUq4rxfE1xM2ZVP9SaWotVSKMqfeDG8ZTTpD8rCp2e9sx/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oozvBvxUq4rxfE1xM2ZVP9SaWotVSKMqfeDG8ZTTpD8rCp2e9sx/unsigned.json'))
        self.assertEqual(expected, actual)
