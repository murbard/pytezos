from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopRZUT(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opRZUT(self):
        expected = get_data(
            path='operations/opRZUTeu2ECPk9kUih3CMCVHZz1FJNk2JQ6ni9QccrWTgaKjHQT/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opRZUTeu2ECPk9kUih3CMCVHZz1FJNk2JQ6ni9QccrWTgaKjHQT/unsigned.json'))
        self.assertEqual(expected, actual)
