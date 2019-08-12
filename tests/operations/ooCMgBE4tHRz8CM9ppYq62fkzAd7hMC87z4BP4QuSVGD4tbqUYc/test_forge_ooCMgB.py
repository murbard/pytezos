from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooCMgB(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooCMgB(self):
        expected = get_data(
            path='operations/ooCMgBE4tHRz8CM9ppYq62fkzAd7hMC87z4BP4QuSVGD4tbqUYc/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooCMgBE4tHRz8CM9ppYq62fkzAd7hMC87z4BP4QuSVGD4tbqUYc/unsigned.json'))
        self.assertEqual(expected, actual)
