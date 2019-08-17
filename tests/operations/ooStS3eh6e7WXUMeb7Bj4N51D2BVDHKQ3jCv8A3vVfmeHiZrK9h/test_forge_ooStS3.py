from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooStS3(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooStS3(self):
        expected = get_data(
            path='operations/ooStS3eh6e7WXUMeb7Bj4N51D2BVDHKQ3jCv8A3vVfmeHiZrK9h/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooStS3eh6e7WXUMeb7Bj4N51D2BVDHKQ3jCv8A3vVfmeHiZrK9h/unsigned.json'))
        self.assertEqual(expected, actual)
