from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoozALX(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oozALX(self):
        expected = get_data(
            path='operations/oozALXdGgRaH8Vrfa8cruqEWor3oAAP5yQMGWLWaBE4DrHkhMS9/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oozALXdGgRaH8Vrfa8cruqEWor3oAAP5yQMGWLWaBE4DrHkhMS9/unsigned.json'))
        self.assertEqual(expected, actual)
