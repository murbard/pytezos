from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopJe44(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opJe44(self):
        expected = get_data(
            path='operations/opJe441zYxMfwFmVquZY1YtTy8eH4U7MTJKF8DkMA1nAzy3E85m/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opJe441zYxMfwFmVquZY1YtTy8eH4U7MTJKF8DkMA1nAzy3E85m/unsigned.json'))
        self.assertEqual(expected, actual)
