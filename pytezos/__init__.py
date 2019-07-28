from pytezos.rpc import alphanet
from pytezos.crypto import Key
from pytezos.client import PyTezosClient

please_use_with_care = Key.from_key('edsk33N474hxzA4sKeWVM6iuGNGDpX2mGwHNxEA4UbWS8sW3Ta3NKH')
pytezos = PyTezosClient(shell=alphanet, key=please_use_with_care)
