from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonhNF4(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onhNF4(self):
        expected = get_data(
            path='operations/onhNF4QiWfoqhLKYZePaGzK8SLwssxYpCrxtxb515oKwaDkoj24/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onhNF4QiWfoqhLKYZePaGzK8SLwssxYpCrxtxb515oKwaDkoj24/unsigned.json'))
        self.assertEqual(expected, actual)
