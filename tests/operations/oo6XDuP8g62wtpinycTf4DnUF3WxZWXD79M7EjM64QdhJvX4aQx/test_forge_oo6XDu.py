from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo6XDu(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo6XDu(self):
        expected = get_data(
            path='operations/oo6XDuP8g62wtpinycTf4DnUF3WxZWXD79M7EjM64QdhJvX4aQx/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo6XDuP8g62wtpinycTf4DnUF3WxZWXD79M7EjM64QdhJvX4aQx/unsigned.json'))
        self.assertEqual(expected, actual)
