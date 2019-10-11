from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopaURa(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opaURa(self):
        expected = get_data(
            path='operations/opaURaapeGBp3uG9k8V9megr8X9w1am7A8w2mqYZEufSeFCEtRY/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opaURaapeGBp3uG9k8V9megr8X9w1am7A8w2mqYZEufSeFCEtRY/unsigned.json'))
        self.assertEqual(expected, actual)
