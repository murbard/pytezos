from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoow7L8(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oow7L8(self):
        expected = get_data(
            path='operations/oow7L897mGvSGTVEQn88pcpikbAJRMgWo73UKMMyo7GdnUpYx5e/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oow7L897mGvSGTVEQn88pcpikbAJRMgWo73UKMMyo7GdnUpYx5e/unsigned.json'))
        self.assertEqual(expected, actual)
