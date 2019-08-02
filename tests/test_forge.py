from unittest import TestCase
from pytezos.operation.forge import forge_reveal, forge_transaction, forge_origination, forge_delegation


class TestOperationEncoding(TestCase):

    def test_reveal(self):
        reveal = {
            "kind": "reveal",
            "source": "tz1VJAdH2HRUZWfohXW59NPYQKFMe1csroaX",
            "fee": "0",
            "counter": "425748",
            "storage_limit": "0",
            "gas_limit": "10000",
            "public_key": "edpkuDuXgPVJi3YK2GKL6avAK3GyjqyvpJjG9gTY5r2y72R7Teo65i"
        }
        expected = b'\x07\x00\x00i\xef\x8f\xb5\xd4}\x8aC!\xc9Ev\xa21jc+\xe8\xce\x89\x00\x94\xfe\x19\x90N\x00\x00L{\x05\x01\xf6\xea\x08\xf4r\xb7\xe8\x87\x91\xd3\xb8\xdaI\xd6J\xc1\xe2\xc9\x0f\x93\xc2~e1G3\x05\xc6'
        self.assertEqual(expected, forge_reveal(reveal))

    def test_transaction(self):
        transaction = {
            "kind": "transaction",
            "source": "tz1VJAdH2HRUZWfohXW59NPYQKFMe1csroaX",
            "fee": "10000",
            "counter": "9",
            "storage_limit": "10001",
            "gas_limit": "10002",
            "amount": "10000000",
            "destination": "tz2G4TwEbsdFrJmApAxJ1vdQGmADnBp95n9m"
        }
        expected = b'\x08\x00\x00i\xef\x8f\xb5\xd4}\x8aC!\xc9Ev\xa21jc+\xe8\xce\x89\x90N\t\x92N\x91N\x80\xad\xe2\x04\x00\x01T\xf5\xd8\xf7\x1c\xe1\x8f\x9f\x05\xbb\x88ZA \xe6Lf{\xc1\xb4\x00'
        self.assertEqual(expected, forge_transaction(transaction))

    def test_transaction_with_parameters(self):
        transaction = {
            "kind": "transaction",
            "source": "tz1eDV7PxrCz2FeyB37C9S7F2KWi2KVYQb1y",
            "fee": "50000",
            "counter": "33446",
            "storage_limit": "60000",
            "gas_limit": "400000",
            "amount": "0",
            "destination": "KT1E7xh6tvnVMWx7QCZnuWXwcpCJ9UmMWcyK",
            "parameters": {"prim": "Left", "args": [ { "prim": "Right", "args": [ { "prim": "Right", "args": [ { "prim": "Right", "args": [ { "prim": "Left", "args": [ { "string": "KT1GE2AZhazRxGsAjRVkQccHcB2pvANXQWd7" } ] } ] } ] } ] } ] }
        }
        expected = b'\x08\x00\x00\xcb\xc6\x0bAS_\xf0GO\xbd\xac\xc4\xe3\xd6X\xee\xd9p~\xbd\xd0\x86\x03\xa6\x85\x02\x80\xb5\x18\xe0\xd4\x03\x00\x01<\xbe\xcf\xc9\x94 \xac,h\x98\xe7\x03*\xaaDyf\xf8\xcef\x00\xff\x00\x00\x003\x05\x05\x05\x08\x05\x08\x05\x08\x05\x05\x01\x00\x00\x00$KT1GE2AZhazRxGsAjRVkQccHcB2pvANXQWd7'
        self.assertEqual(expected, forge_transaction(transaction))

    def test_transaction_with_int_parameters(self):
        transaction = {
            "kind": "transaction",
            "source": "tz1LBEKXaxQbd5Gtzbc1ATCwc3pppu81aWGc",
            "fee": "20074",
            "counter": "76765",
            "storage_limit": "0",
            "gas_limit": "197883",
            "amount": "0",
            "destination": "KT1BvVxWM6cjFuJNet4R9m64VDCN2iMvjuGE",
            "parameters": {"prim": "Right", "args": [{"prim": "Right", "args": [{"prim": "Right", "args": [{"prim": "Right", "args": [{"prim": "Pair", "args": [{"int": "1062060"}, {"prim": "Pair", "args": [{"int": "1062727"}, {"int": "362230136"}]}]}]}]}]}]}
        }
        expected = b"\x08\x00\x00\x05\xe6\x99\xe5\xeb\xd7\x9aY\x19\x98\xa1\xd8\xb3\xf2\x936l\xf0\x0b\xbb\xea\x9c\x01\xdd\xd7\x04\xfb\x89\x0c\x00\x00\x01$\xa3\xaa\xf2y9\x10\xa3\xbf5\xa4\xae72\x88\x9e\xe4Z\n\xba\x00\xff\x00\x00\x00\x1c\x05\x08\x05\x08\x05\x08\x05\x08\x07\x07\x00\xac\xd2\x81\x01\x07\x07\x00\x87\xdd\x81\x01\x00\xb8\xc5\xb9\xd9\x02"
        self.assertEqual(expected, forge_transaction(transaction))

    def test_transaction_with_bytes_parameters(self):
        transaction = {
            "kind": "transaction",
            "source": "tz1b1LEzNxq3auDZBWMXcPMX6riBVxGAs65q",
            "fee": "50000",
            "counter": "2201",
            "storage_limit": "20",
            "gas_limit": "161926",
            "amount": "0",
            "destination": "KT1QdevirZq7PpMgVFWP6QVRSGbSsdHEUjgt",
            "parameters": {"prim": "Left", "args": [{"prim": "Right", "args": [{"prim": "Left", "args": [{"bytes": "a856040505b00983d402c61599c35c2c3419d2d8"}]}]}]}
        }
        expected = b"\x08\x00\x00\xa8\x91E\x83\x80\x81]\x89;\xeb\x7f\xdc\xa9|\xa1\xab]\xd2\x1e\x02\xd0\x86\x03\x99\x11\x86\xf1\t\x14\x00\x01\xb0\r\xb7\xffu\xb3\x1c\xe5\xba\x05\x01\xc3'\xa9\xd4\x11\xae\x97\x7fU\x00\xff\x00\x00\x00\x1f\x05\x05\x05\x08\x05\x05\n\x00\x00\x00\x14\xa8V\x04\x05\x05\xb0\t\x83\xd4\x02\xc6\x15\x99\xc3\\,4\x19\xd2\xd8"
        self.assertEqual(expected, forge_transaction(transaction))

    def test_origination(self):
        origination = {
            "kind": "origination",
            "source": "tz1VJAdH2HRUZWfohXW59NPYQKFMe1csroaX",
            "fee": "10000",
            "counter": "9",
            "storage_limit": "10001",
            "gas_limit": "10002",
            "manager_pubkey": "tz1VJAdH2HRUZWfohXW59NPYQKFMe1csroaX",
            "balance": "10003",
            "spendable": True,
            "delegatable": True,
            "delegate": "tz1VJAdH2HRUZWfohXW59NPYQKFMe1csroaX"
        }
        expected = b'\t\x00\x00i\xef\x8f\xb5\xd4}\x8aC!\xc9Ev\xa21jc+\xe8\xce\x89\x90N\t\x92N\x91N\x00i\xef\x8f\xb5\xd4}\x8aC!\xc9Ev\xa21jc+\xe8\xce\x89\x93N\xff\xff\xff\x00i\xef\x8f\xb5\xd4}\x8aC!\xc9Ev\xa21jc+\xe8\xce\x89\x00'
        self.assertEqual(expected, forge_origination(origination))

    def test_origination_with_script(self):
        origination = {
            'kind': 'origination',
            'source': 'tz1Z1nn9Y7vzyvtf6rAYMPhPNGqMJXw88xGH',
            'fee': '3884',
            'counter': '23015',
            'gas_limit': '28461',
            'storage_limit': '1059',
            'manager_pubkey': 'tz1Z1nn9Y7vzyvtf6rAYMPhPNGqMJXw88xGH',
            'balance': '0',
            'spendable': False,
            'delegatable': False,
            'script': {"code": [{"prim": "parameter", "args": [{"prim": "or","args": [{"prim": "pair","args": [{"prim": "address"}, {"prim": "michelson",  "args": [{"prim": "or", "args": [{"prim": "pair", "args": [{"prim": "address"},  {"prim": "pair","args": [{"prim": "address"}, {"prim": "nat"}]}]},{"prim": "address"}]}]}]}, {"prim": "nat"}]}]},{"prim": "storage", "args": [{"prim": "pair","args": [{"prim": "big_map","args": [{"prim": "address"}, {"prim": "pair",  "args": [{"prim": "mutez"}, {"prim": "address"}]}]}, {"prim": "unit"}]}]},{"prim": "code", "args": [[{"prim": "DUP"},{"prim": "CAR"},{"prim": "DIP", "args": [[{"prim": "CDR"}]]},{"prim": "IF_LEFT", "args": [[{"prim": "DUP"}, {"prim": "CDR"}, {"prim": "DIP", "args": [[{"prim": "SWAP"}]]}, {"prim": "DIP",  "args": [[{"prim": "SENDER"}, {"prim": "CONTRACT","args": [{"prim": "or",  "args": [{"prim": "or", "args": [{"prim": "or", "args": [{"prim": "pair","args": [{"prim": "nat"}, {"prim": "pair","args": [{"prim": "nat"}, {"prim": "timestamp"}]}]},  {"prim": "nat"}]},{"prim": "or", "args": [{"prim": "pair","args": [{"prim": "pair","args": [{"prim": "nat"}, {"prim": "mutez"}]}, {"prim": "pair","args": [{"prim": "nat"}, {"prim": "timestamp"}]}]},  {"prim": "nat"}]}]},{"prim": "or", "args": [{"prim": "pair", "args": [{"prim": "nat"}, {"prim": "timestamp"}]},{"prim": "nat"}]}]}]}, {"prim": "IF_NONE","args": [[{"prim": "PUSH","args": [{"prim": "string"}, {"string": "removeLiquidityToGetBalance: sender michelson does not match the expected type."}]},  {"prim": "FAILWITH"}], []]}]]}, {"prim": "ADDRESS"}, {"prim": "DIP",  "args": [[{"prim": "ADDRESS"}, {"prim": "AMOUNT"}, {"prim": "PAIR", "annots": ["%", "%"]}, {"prim": "SOME"}, {"prim": "DIP", "args": [[{"prim": "DUP"}, {"prim": "CAR"}]]}]]}, {"prim": "UPDATE"}, {"prim": "DIP",  "args": [[{"prim": "DUP"}, {"prim": "DIP", "args": [[{"prim": "CDR"}]]}, {"prim": "CAR"}]]}, {"prim": "DIP", "args": [[{"prim": "DROP"}]]}, {"prim": "PAIR", "annots": ["%", "%"]}, {"prim": "SWAP"}, {"prim": "DUP"}, {"prim": "CAR"}, {"prim": "RIGHT",  "args": [{"prim": "pair", "args": [{"prim": "address"},{"prim": "pair", "args": [{"prim": "address"}, {"prim": "nat"}]}]}],  "annots": ["%", "%"]}, {"prim": "DIP",  "args": [[{"prim": "CDR"}, {"prim": "PUSH", "args": [{"prim": "mutez"}, {"int": "0"}]}]]}, {"prim": "TRANSFER_TOKENS"}, {"prim": "NIL", "args": [{"prim": "operation"}]}, {"prim": "SWAP"}, {"prim": "CONS"}, {"prim": "PAIR", "annots": ["%", "%"]}],[{"prim": "RIGHT", "args": [{"prim": "pair", "args": [{"prim": "nat"}, {"prim": "timestamp"}]}],  "annots": ["%", "%"]}, {"prim": "RIGHT",  "args": [{"prim": "or", "args": [{"prim": "or", "args": [{"prim": "pair","args": [{"prim": "nat"}, {"prim": "pair","args": [{"prim": "nat"}, {"prim": "timestamp"}]}]},  {"prim": "nat"}]},{"prim": "or", "args": [{"prim": "pair","args": [{"prim": "pair","args": [{"prim": "nat"}, {"prim": "mutez"}]}, {"prim": "pair","args": [{"prim": "nat"}, {"prim": "timestamp"}]}]},  {"prim": "nat"}]}]}],  "annots": ["%", "%"]}, {"prim": "DIP",  "args": [[{"prim": "SENDER"}, {"prim": "DIP", "args": [[{"prim": "DUP"}, {"prim": "CAR"}]]}, {"prim": "GET"}, {"prim": "IF_NONE","args": [[{"prim": "PUSH","args": [{"prim": "string"}, {"string": "getBalanceToRemoveLiquidity: unexpected, exchange not found for existing token michelson."}]},  {"prim": "FAILWITH"}], []]}, {"prim": "DUP"}, {"prim": "CAR"}, {"prim": "DIP", "args": [[{"prim": "CDR"}]]}, {"prim": "DIP","args": [[{"prim": "CONTRACT","args": [{"prim": "or","args": [{"prim": "or",  "args": [{"prim": "or", "args": [{"prim": "pair", "args": [{"prim": "nat"},  {"prim": "pair","args": [{"prim": "nat"}, {"prim": "timestamp"}]}]},{"prim": "nat"}]},{"prim": "or", "args": [{"prim": "pair", "args": [{"prim": "pair","args": [{"prim": "nat"}, {"prim": "mutez"}]},  {"prim": "pair","args": [{"prim": "nat"}, {"prim": "timestamp"}]}]},{"prim": "nat"}]}]}, {"prim": "or",  "args": [{"prim": "pair", "args": [{"prim": "nat"}, {"prim": "timestamp"}]},{"prim": "nat"}]}]}]},  {"prim": "IF_NONE","args": [[{"prim": "PUSH", "args": [{"prim": "string"},  {"string": "getBalanceToRemoveLiquidity: exchange michelson does not match the expected type."}]},{"prim": "FAILWITH"}], []]}]]}]]}, {"prim": "TRANSFER_TOKENS"}, {"prim": "NIL", "args": [{"prim": "operation"}]}, {"prim": "SWAP"}, {"prim": "CONS"}, {"prim": "PAIR", "annots": ["%", "%"]}]]}]]}], "storage": {"prim": "Pair", "args": [[], {"prim": "Unit"}]}}
        }
        expected = b'\t\x00\x00\x92\xb7,\x0f\xa1\x06C1\xa6A\x13\x1fW.\x7f*\xbb\x9a\x89\x0b\xac\x1e\xe7\xb3\x01\xad\xde\x01\xa3\x08\x00\x92\xb7,\x0f\xa1\x06C1\xa6A\x13\x1fW.\x7f*\xbb\x9a\x89\x0b\x00\x00\x00\x00\xff\x00\x00\x02\xfd\x02\x00\x00\x02\xf8\x05\x00\x07d\x07e\x03n\x05Z\x07d\x07e\x03n\x07e\x03n\x03b\x03n\x03b\x05\x01\x07e\x07a\x03n\x07e\x03j\x03n\x03l\x05\x02\x02\x00\x00\x02\xc7\x03!\x03\x16\x05\x1f\x02\x00\x00\x00\x02\x03\x17\x07.\x02\x00\x00\x011\x03!\x03\x17\x05\x1f\x02\x00\x00\x00\x02\x03L\x05\x1f\x02\x00\x00\x00\x97\x03H\x05U\x07d\x07d\x07d\x07e\x03b\x07e\x03b\x03k\x03b\x07d\x07e\x07e\x03b\x03j\x07e\x03b\x03k\x03b\x07d\x07e\x03b\x03k\x03b\x07/\x02\x00\x00\x00Y\x07C\x03h\x01\x00\x00\x00NremoveLiquidityToGetBalance: sender michelson does not match the expected type.\x03\'\x02\x00\x00\x00\x00\x03T\x05\x1f\x02\x00\x00\x00\x1a\x03T\x03\x13\x04B\x00\x00\x00\x03% %\x03F\x05\x1f\x02\x00\x00\x00\x04\x03!\x03\x16\x03P\x05\x1f\x02\x00\x00\x00\r\x03!\x05\x1f\x02\x00\x00\x00\x02\x03\x17\x03\x16\x05\x1f\x02\x00\x00\x00\x02\x03 \x04B\x00\x00\x00\x03% %\x03L\x03!\x03\x16\x06D\x07e\x03n\x07e\x03n\x03b\x00\x00\x00\x03% %\x05\x1f\x02\x00\x00\x00\x08\x03\x17\x07C\x03j\x00\x00\x03M\x05=\x03m\x03L\x03\x1b\x04B\x00\x00\x00\x03% %\x02\x00\x00\x01}\x06D\x07e\x03b\x03k\x00\x00\x00\x03% %\x06D\x07d\x07d\x07e\x03b\x07e\x03b\x03k\x03b\x07d\x07e\x07e\x03b\x03j\x07e\x03b\x03k\x03b\x00\x00\x00\x03% %\x05\x1f\x02\x00\x00\x01)\x03H\x05\x1f\x02\x00\x00\x00\x04\x03!\x03\x16\x03)\x07/\x02\x00\x00\x00c\x07C\x03h\x01\x00\x00\x00XgetBalanceToRemoveLiquidity: unexpected, exchange not found for existing token michelson.\x03\'\x02\x00\x00\x00\x00\x03!\x03\x16\x05\x1f\x02\x00\x00\x00\x02\x03\x17\x05\x1f\x02\x00\x00\x00\x97\x05U\x07d\x07d\x07d\x07e\x03b\x07e\x03b\x03k\x03b\x07d\x07e\x07e\x03b\x03j\x07e\x03b\x03k\x03b\x07d\x07e\x03b\x03k\x03b\x07/\x02\x00\x00\x00[\x07C\x03h\x01\x00\x00\x00PgetBalanceToRemoveLiquidity: exchange michelson does not match the expected type.\x03\'\x02\x00\x00\x00\x00\x03M\x05=\x03m\x03L\x03\x1b\x04B\x00\x00\x00\x03% %\x00\x00\x00\t\x07\x07\x02\x00\x00\x00\x00\x03\x0b'
        self.assertEqual(expected, forge_origination(origination))

    def test_delegation(self):
        delegation = {
            "kind": "delegation",
            "source": "tz1VJAdH2HRUZWfohXW59NPYQKFMe1csroaX",
            "fee": "10000",
            "counter": "9",
            "storage_limit": "10001",
            "gas_limit": "10002",
            "delegate": 'tz3WXYtyDUNL91qfiCJtVUX746QpNv5i5ve5'
        }
        expected = b'\n\x00\x00i\xef\x8f\xb5\xd4}\x8aC!\xc9Ev\xa21jc+\xe8\xce\x89\x90N\t\x92N\x91N\xff\x02o\xdeF\xaf\x03V\xa0Gm\xaeNF\x00\x17-\xc90\x9b:\xa4'
        self.assertEqual(expected, forge_delegation(delegation))
