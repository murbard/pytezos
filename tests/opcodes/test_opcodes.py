from os.path import dirname, join
from unittest import TestCase
from parameterized import parameterized

from pytezos.repl.interpreter import Interpreter


def abs_path(filename):
    return join(dirname(__file__), filename)


class TestOpcodes(TestCase):

    def setUp(self):
        self.i = Interpreter(debug=True)

    def include(self, filename):
        res = self.i.execute(f'INCLUDE "{abs_path(filename)}"')
        self.assertTrue(res['success'])

    def test_abs(self):
        self.include('abs.tz')
        res = self.i.execute('RUN 42 Unit')
        self.assertTrue(res['success'])

    def test_add(self):
        self.include('add.tz')
        res = self.i.execute('RUN Unit Unit')
        self.assertTrue(res['success'])

    def test_add_delta_timestamp(self):
        self.include('add_delta_timestamp.tz')
        res = self.i.execute('RUN (Pair 0 0) (Some 0)')
        self.assertTrue(res['success'])

    @parameterized.expand([
        ('RUN (Pair 100 100) (Some "1970-01-01T00:03:20Z")',),
        ('RUN (Pair 100 -100) (Some "1970-01-01T00:00:00Z")',),
        ('RUN (Pair "1970-01-01T00:00:00Z" 0) (Some "1970-01-01T00:00:00Z")',)
    ])
    def test_add_timestamp_delta(self, expr):
        self.include('add_timestamp_delta.tz')
        res = self.i.execute(expr)
        self.assertTrue(res['success'])
