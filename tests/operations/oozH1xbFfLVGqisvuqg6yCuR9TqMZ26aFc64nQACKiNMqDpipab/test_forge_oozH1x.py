from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoozH1x(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oozH1x(self):
        expected = get_data(
            path='operations/oozH1xbFfLVGqisvuqg6yCuR9TqMZ26aFc64nQACKiNMqDpipab/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oozH1xbFfLVGqisvuqg6yCuR9TqMZ26aFc64nQACKiNMqDpipab/unsigned.json'))
        self.assertEqual(expected, actual)
