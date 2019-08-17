from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonud8a(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onud8a(self):
        expected = get_data(
            path='operations/onud8aRdr265yY29ZSXtTV3BEhVaHivJUKzMb2dzrVHSVx2sBC6/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onud8aRdr265yY29ZSXtTV3BEhVaHivJUKzMb2dzrVHSVx2sBC6/unsigned.json'))
        self.assertEqual(expected, actual)
