from unittest import TestCase

from pytezos.repl.interpreter import Interpreter
from pytezos.michelson.converter import michelson_to_micheline
from pytezos.repl.parser import parse_value


class OpcodeTestediv_mutez_232(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.i = Interpreter(debug=True)
        
    def test_opcode_ediv_mutez_232(self):
        res = self.i.execute('INCLUDE "/home/mickey/pytezos/tests/opcodes/contracts/ediv_mutez.tz"')
        self.assertTrue(res['success'])
        
        res = self.i.execute('RUN (Pair 10 (Right 10)) (Left None)')
        self.assertTrue(res['success'])
        
        type_expr = self.i.ctx.stack[0].type_expr['args'][1]
        expected_expr = michelson_to_micheline('(Right (Some (Pair 1 0)))')
        expected_val = parse_value(expected_expr, type_expr)
        self.assertEqual(expected_val, self.i.ctx.stack[0]._val[1])