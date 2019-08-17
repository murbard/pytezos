from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoneKi3(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oneKi3(self):
        expected = get_data(
            path='operations/oneKi3Xd4wWkzpvLgCkMzAi4KCFVnezY75HncPzg7zngAUwMfwo/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oneKi3Xd4wWkzpvLgCkMzAi4KCFVnezY75HncPzg7zngAUwMfwo/unsigned.json'))
        self.assertEqual(expected, actual)
