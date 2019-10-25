from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooUcc3(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooUcc3(self):
        expected = get_data(
            path='operations/ooUcc3rRWkhMmPiV89ktr58rPj7kchEGfYrk71VbpcUKNVuF7GU/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooUcc3rRWkhMmPiV89ktr58rPj7kchEGfYrk71VbpcUKNVuF7GU/unsigned.json'))
        self.assertEqual(expected, actual)
