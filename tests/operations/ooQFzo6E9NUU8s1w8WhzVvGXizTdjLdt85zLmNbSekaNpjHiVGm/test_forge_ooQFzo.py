from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooQFzo(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooQFzo(self):
        expected = get_data(
            path='operations/ooQFzo6E9NUU8s1w8WhzVvGXizTdjLdt85zLmNbSekaNpjHiVGm/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooQFzo6E9NUU8s1w8WhzVvGXizTdjLdt85zLmNbSekaNpjHiVGm/unsigned.json'))
        self.assertEqual(expected, actual)
