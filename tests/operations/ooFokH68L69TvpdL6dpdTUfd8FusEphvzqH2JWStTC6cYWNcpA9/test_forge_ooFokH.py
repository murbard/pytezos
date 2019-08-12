from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooFokH(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooFokH(self):
        expected = get_data(
            path='operations/ooFokH68L69TvpdL6dpdTUfd8FusEphvzqH2JWStTC6cYWNcpA9/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooFokH68L69TvpdL6dpdTUfd8FusEphvzqH2JWStTC6cYWNcpA9/unsigned.json'))
        self.assertEqual(expected, actual)
