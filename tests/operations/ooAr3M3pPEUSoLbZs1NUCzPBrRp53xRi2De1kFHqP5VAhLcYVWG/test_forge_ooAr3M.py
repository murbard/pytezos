from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooAr3M(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooAr3M(self):
        expected = get_data(
            path='operations/ooAr3M3pPEUSoLbZs1NUCzPBrRp53xRi2De1kFHqP5VAhLcYVWG/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooAr3M3pPEUSoLbZs1NUCzPBrRp53xRi2De1kFHqP5VAhLcYVWG/unsigned.json'))
        self.assertEqual(expected, actual)
