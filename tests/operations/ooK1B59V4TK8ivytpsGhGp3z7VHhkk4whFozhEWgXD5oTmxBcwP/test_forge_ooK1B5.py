from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooK1B5(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooK1B5(self):
        expected = get_data(
            path='operations/ooK1B59V4TK8ivytpsGhGp3z7VHhkk4whFozhEWgXD5oTmxBcwP/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooK1B59V4TK8ivytpsGhGp3z7VHhkk4whFozhEWgXD5oTmxBcwP/unsigned.json'))
        self.assertEqual(expected, actual)
