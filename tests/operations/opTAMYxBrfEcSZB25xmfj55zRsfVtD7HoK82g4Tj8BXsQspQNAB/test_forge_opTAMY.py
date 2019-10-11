from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopTAMY(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opTAMY(self):
        expected = get_data(
            path='operations/opTAMYxBrfEcSZB25xmfj55zRsfVtD7HoK82g4Tj8BXsQspQNAB/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opTAMYxBrfEcSZB25xmfj55zRsfVtD7HoK82g4Tj8BXsQspQNAB/unsigned.json'))
        self.assertEqual(expected, actual)
