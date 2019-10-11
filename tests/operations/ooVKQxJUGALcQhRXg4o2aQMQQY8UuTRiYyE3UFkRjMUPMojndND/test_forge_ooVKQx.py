from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooVKQx(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooVKQx(self):
        expected = get_data(
            path='operations/ooVKQxJUGALcQhRXg4o2aQMQQY8UuTRiYyE3UFkRjMUPMojndND/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooVKQxJUGALcQhRXg4o2aQMQQY8UuTRiYyE3UFkRjMUPMojndND/unsigned.json'))
        self.assertEqual(expected, actual)
