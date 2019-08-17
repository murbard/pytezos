from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoouHvZ(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oouHvZ(self):
        expected = get_data(
            path='operations/oouHvZoHxJZ6Qrn9ZQR8fCyDJkF9YW2o958B34oNmMm9gUhoicb/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oouHvZoHxJZ6Qrn9ZQR8fCyDJkF9YW2o958B34oNmMm9gUhoicb/unsigned.json'))
        self.assertEqual(expected, actual)
