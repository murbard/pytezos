from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooxWuv(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooxWuv(self):
        expected = get_data(
            path='operations/ooxWuvHaRfeKQgSzswqBdaJ7vdGFCkKnUrzKhgKLUapCt2suSQP/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooxWuvHaRfeKQgSzswqBdaJ7vdGFCkKnUrzKhgKLUapCt2suSQP/unsigned.json'))
        self.assertEqual(expected, actual)
