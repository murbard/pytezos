from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo9PRH(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo9PRH(self):
        expected = get_data(
            path='operations/oo9PRHqqjYB89atKsUjUyXMcWQRnG9FK9yRkXwdRRokdTr4LgGT/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo9PRHqqjYB89atKsUjUyXMcWQRnG9FK9yRkXwdRRokdTr4LgGT/unsigned.json'))
        self.assertEqual(expected, actual)
