from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo8CvP(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo8CvP(self):
        expected = get_data(
            path='operations/oo8CvPu2z41vCUfb3szH3udVnipnnUNwj3X5EXf5eM7WV468eS4/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo8CvPu2z41vCUfb3szH3udVnipnnUNwj3X5EXf5eM7WV468eS4/unsigned.json'))
        self.assertEqual(expected, actual)
