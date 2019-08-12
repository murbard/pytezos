from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopU4vu(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opU4vu(self):
        expected = get_data(
            path='operations/opU4vuARUmQTmFnZkejpdmJpT8J9iTz2Tq4Q83u3Nx8uiumDxhw/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opU4vuARUmQTmFnZkejpdmJpT8J9iTz2Tq4Q83u3Nx8uiumDxhw/unsigned.json'))
        self.assertEqual(expected, actual)
