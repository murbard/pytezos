from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoovqY8(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oovqY8(self):
        expected = get_data(
            path='operations/oovqY8B3bUMHuk5eb8BdMrzrHej6wSRAfSkFBzHaQtaPLriWWyc/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oovqY8B3bUMHuk5eb8BdMrzrHej6wSRAfSkFBzHaQtaPLriWWyc/unsigned.json'))
        self.assertEqual(expected, actual)
