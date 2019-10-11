from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonsJaC(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onsJaC(self):
        expected = get_data(
            path='operations/onsJaC4W5qS3mKvhDa3jSuLcKabNrNefnMgJBhF2sJAuiiS9gtp/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onsJaC4W5qS3mKvhDa3jSuLcKabNrNefnMgJBhF2sJAuiiS9gtp/unsigned.json'))
        self.assertEqual(expected, actual)
