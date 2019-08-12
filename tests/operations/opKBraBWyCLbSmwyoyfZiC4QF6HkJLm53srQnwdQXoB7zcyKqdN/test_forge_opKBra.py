from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopKBra(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opKBra(self):
        expected = get_data(
            path='operations/opKBraBWyCLbSmwyoyfZiC4QF6HkJLm53srQnwdQXoB7zcyKqdN/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opKBraBWyCLbSmwyoyfZiC4QF6HkJLm53srQnwdQXoB7zcyKqdN/unsigned.json'))
        self.assertEqual(expected, actual)
