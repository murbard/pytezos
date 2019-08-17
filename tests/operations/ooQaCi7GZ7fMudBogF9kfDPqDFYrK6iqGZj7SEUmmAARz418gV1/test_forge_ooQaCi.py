from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooQaCi(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooQaCi(self):
        expected = get_data(
            path='operations/ooQaCi7GZ7fMudBogF9kfDPqDFYrK6iqGZj7SEUmmAARz418gV1/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooQaCi7GZ7fMudBogF9kfDPqDFYrK6iqGZj7SEUmmAARz418gV1/unsigned.json'))
        self.assertEqual(expected, actual)
