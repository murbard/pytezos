from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoofYWv(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oofYWv(self):
        expected = get_data(
            path='operations/oofYWvALzXQkqTsPMY7rgKGYA7M4rvctK2o51LTS1g8yB7tfrWm/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oofYWvALzXQkqTsPMY7rgKGYA7M4rvctK2o51LTS1g8yB7tfrWm/unsigned.json'))
        self.assertEqual(expected, actual)
