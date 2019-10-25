from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopWpmh(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opWpmh(self):
        expected = get_data(
            path='operations/opWpmhZf4L7wDV6SHmWeV2gb47iEMehndhK1NtgRSgJPr1Udaf6/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opWpmhZf4L7wDV6SHmWeV2gb47iEMehndhK1NtgRSgJPr1Udaf6/unsigned.json'))
        self.assertEqual(expected, actual)
