from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonkxSi(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onkxSi(self):
        expected = get_data(
            path='operations/onkxSiohubQAMhvRXUemnxF6iivXfNFHWxcSa4GJZGWA1VHNsD2/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onkxSiohubQAMhvRXUemnxF6iivXfNFHWxcSa4GJZGWA1VHNsD2/unsigned.json'))
        self.assertEqual(expected, actual)
