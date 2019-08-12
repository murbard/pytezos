from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooqoNq(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooqoNq(self):
        expected = get_data(
            path='operations/ooqoNqqhZaaoEeeFDe6xB3fHsv76uMfYRaPGx1HiY36KD1U7n8y/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooqoNqqhZaaoEeeFDe6xB3fHsv76uMfYRaPGx1HiY36KD1U7n8y/unsigned.json'))
        self.assertEqual(expected, actual)
