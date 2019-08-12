from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo7pg2(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo7pg2(self):
        expected = get_data(
            path='operations/oo7pg2ftJaEBFh1Eh7HBntTFuc4gKvp4pGsXHzP7XoicyfXxeds/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo7pg2ftJaEBFh1Eh7HBntTFuc4gKvp4pGsXHzP7XoicyfXxeds/unsigned.json'))
        self.assertEqual(expected, actual)
