from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonhZrs(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onhZrs(self):
        expected = get_data(
            path='operations/onhZrswP8gg3EnwadkMjK5BjaKiJKoP5YzbHxypTeonGUgHTkVX/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onhZrswP8gg3EnwadkMjK5BjaKiJKoP5YzbHxypTeonGUgHTkVX/unsigned.json'))
        self.assertEqual(expected, actual)
