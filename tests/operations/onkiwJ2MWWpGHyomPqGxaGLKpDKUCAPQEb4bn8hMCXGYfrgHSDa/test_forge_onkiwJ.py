from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonkiwJ(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onkiwJ(self):
        expected = get_data(
            path='operations/onkiwJ2MWWpGHyomPqGxaGLKpDKUCAPQEb4bn8hMCXGYfrgHSDa/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onkiwJ2MWWpGHyomPqGxaGLKpDKUCAPQEb4bn8hMCXGYfrgHSDa/unsigned.json'))
        self.assertEqual(expected, actual)
