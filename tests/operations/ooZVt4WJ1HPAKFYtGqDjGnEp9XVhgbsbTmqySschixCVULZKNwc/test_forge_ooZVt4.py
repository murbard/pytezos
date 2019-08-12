from unittest import TestCase

from tests import get_data
from pytezos.operation.forge import forge_operation_group


class OperationForgingTestooZVt4(TestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_forge_ooZVt4(self):
        expected = get_data(
            path='operations/ooZVt4WJ1HPAKFYtGqDjGnEp9XVhgbsbTmqySschixCVULZKNwc/forged.hex')
        actual = forge_operation_group(get_data(
            path='operations/ooZVt4WJ1HPAKFYtGqDjGnEp9XVhgbsbTmqySschixCVULZKNwc/unsigned.json'))
        self.assertEqual(expected, actual)
