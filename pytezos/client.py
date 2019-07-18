from pytezos.rpc import alphanet
from pytezos.tools.keychain import Keychain


class Client:

    def __init__(self, shell=alphanet, keychain=Keychain()):
        self._shell = shell
        self._keychain = keychain

    def