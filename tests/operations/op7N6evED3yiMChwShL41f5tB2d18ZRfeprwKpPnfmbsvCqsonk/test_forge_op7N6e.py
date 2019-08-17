from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestop7N6e(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_op7N6e(self):
        expected = get_data(
            path='operations/op7N6evED3yiMChwShL41f5tB2d18ZRfeprwKpPnfmbsvCqsonk/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/op7N6evED3yiMChwShL41f5tB2d18ZRfeprwKpPnfmbsvCqsonk/unsigned.json'))
        self.assertEqual(expected, actual)
