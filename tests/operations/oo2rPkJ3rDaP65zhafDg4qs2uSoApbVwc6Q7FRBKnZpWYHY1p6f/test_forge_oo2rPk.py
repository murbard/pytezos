from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo2rPk(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo2rPk(self):
        expected = get_data(
            path='operations/oo2rPkJ3rDaP65zhafDg4qs2uSoApbVwc6Q7FRBKnZpWYHY1p6f/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo2rPkJ3rDaP65zhafDg4qs2uSoApbVwc6Q7FRBKnZpWYHY1p6f/unsigned.json'))
        self.assertEqual(expected, actual)
