from contextlib import suppress
from unittest import TestCase
from unittest.mock import MagicMock, patch
from pytezos.client import PyTezosClient


class TestOperation(TestCase):
    @patch("pytezos.rpc.protocol.BlocksQuery.__getitem__")
    def test_fill(self, rpc_mock):
        # Arrange
        testmap = {
            'branch_offset_sandboxed': [5, None, True, -5],
            'branch_offset_not_sandboxed': [5, None, False, -5],
            'ttl_sandboxed': [None, 5, True, -55],
            'ttl_not_sandboxed': [None, 5, False, -55],
            'ttl_sandboxed_default': [None, None, True, -50],
            'ttl_not_sandboxed_default': [None, None, False, 0],
        }

        client = PyTezosClient()
        op = client.transaction(destination='')

        for name, (branch_offset, ttl, sandboxed, mock_call) in testmap.items():
            with self.subTest(name):
                # Act
                op.context._sandboxed = sandboxed
                with suppress(Exception):
                    op.fill(branch_offset=branch_offset, ttl=ttl)

                # Assert
                rpc_mock.assert_called_with(mock_call)
