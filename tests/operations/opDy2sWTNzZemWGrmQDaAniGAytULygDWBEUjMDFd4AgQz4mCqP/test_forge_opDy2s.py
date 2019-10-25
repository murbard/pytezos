from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestopDy2s(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_opDy2s(self):
        expected = get_data(
            path='operations/opDy2sWTNzZemWGrmQDaAniGAytULygDWBEUjMDFd4AgQz4mCqP/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/opDy2sWTNzZemWGrmQDaAniGAytULygDWBEUjMDFd4AgQz4mCqP/unsigned.json'))
        self.assertEqual(expected, actual)
