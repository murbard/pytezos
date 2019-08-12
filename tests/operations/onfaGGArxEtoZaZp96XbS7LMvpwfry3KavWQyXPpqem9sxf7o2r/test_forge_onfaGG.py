from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestonfaGG(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_onfaGG(self):
        expected = get_data(
            path='operations/onfaGGArxEtoZaZp96XbS7LMvpwfry3KavWQyXPpqem9sxf7o2r/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/onfaGGArxEtoZaZp96XbS7LMvpwfry3KavWQyXPpqem9sxf7o2r/unsigned.json'))
        self.assertEqual(expected, actual)
