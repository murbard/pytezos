import os
import simplejson as json
from getpass import getpass
from loguru import logger

from pytezos.crypto import Key
from pytezos.rpc import mainnet


class OTP:

    def __init__(self, key: Key, interval=5, shell=mainnet):
        self._key = key
        self._interval = interval
        self._shell = shell

    def now(self) -> str:
        if not self._key.is_secret:
            raise ValueError('Cannot generate OTP without a secret key')

        message = self._shell.head.hash()
        logger.debug(f'block hash: {message}')

        return self._key.sign(message)

    def verify(self, signature) -> bool:
        block_hashes = self._shell.blocks(length=self._interval)

        for row in block_hashes:
            try:
                message = row[0]
                logger.debug(f'try {message}')

                self._key.verify(signature, message)
            except ValueError as e:
                logger.debug(str(e))
            else:
                return True

        return False


class Keychain:

    def __init__(self, path='~/.tezos-client/secret_keys'):
        self._path = os.path.expanduser(path)
        self._secret_keys = list()
        self._last_modified = 0

    def reload(self):
        last_modified = os.path.getmtime(self._path)
        if last_modified > self._last_modified:
            self._last_modified = last_modified
            with open(self._path, 'r') as f:
                self._secret_keys = json.load(f)

    def get_key(self, name) -> Key:
        self.reload()

        value = next(item['value'] for item in self._secret_keys if item['name'] == name)
        prefix, key = value.split(':', maxsplit=1)

        if prefix == 'encrypted':
            password = getpass(f'Please, enter passphrase for `{name}`:\n')
            key = Key(key, passphrase=password)
        else:
            key = Key(key)

        return key

    def list_keys(self) -> list:
        self.reload()

        def format_item(item: dict):
            prefix, key = item['value'].split(':')
            return dict(
                name=item['name'],
                type=prefix,
                curve={'ed': 'ed25519', 'sp': 'secp256k1', 'p2': 'p256'}[key[:2]]
            )

        return list(map(format_item, self._secret_keys))
