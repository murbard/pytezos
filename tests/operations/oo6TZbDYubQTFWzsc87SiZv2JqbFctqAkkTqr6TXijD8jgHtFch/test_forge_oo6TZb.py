from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestoo6TZb(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_oo6TZb(self):
        expected = get_data(
            path='operations/oo6TZbDYubQTFWzsc87SiZv2JqbFctqAkkTqr6TXijD8jgHtFch/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/oo6TZbDYubQTFWzsc87SiZv2JqbFctqAkkTqr6TXijD8jgHtFch/unsigned.json'))
        self.assertEqual(expected, actual)
