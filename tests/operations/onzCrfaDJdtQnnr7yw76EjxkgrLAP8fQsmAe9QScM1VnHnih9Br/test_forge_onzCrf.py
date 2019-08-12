from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonzCrf(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onzCrf(self):
        expected = get_data(
            path='operations/onzCrfaDJdtQnnr7yw76EjxkgrLAP8fQsmAe9QScM1VnHnih9Br/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onzCrfaDJdtQnnr7yw76EjxkgrLAP8fQsmAe9QScM1VnHnih9Br/unsigned.json'))
        self.assertEqual(expected, actual)
