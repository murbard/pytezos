from os.path import dirname, join
from unittest import TestCase

from pytezos.repl.interpreter import Interpreter


def abs_path(filename):
    return join(dirname(__file__), filename)


class TestOpcodes(TestCase):

    def setUp(self):
        self.i = Interpreter()

    def test_abs(self):
        self.i.execute(f'INCLUDE "{abs_path("abs.tz")}"')
        self.i.execute('RUN 42 Unit')
