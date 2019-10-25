from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoop3eE(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oop3eE(self):
        expected = get_data(
            path='operations/oop3eEJQcM1aNh2G6m1pXSS5mC6wK77XN1wDwrgMehrLM6Nh7cq/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oop3eEJQcM1aNh2G6m1pXSS5mC6wK77XN1wDwrgMehrLM6Nh7cq/unsigned.json'))
        self.assertEqual(expected, actual)
