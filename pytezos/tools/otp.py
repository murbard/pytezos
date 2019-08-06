from loguru import logger

from pytezos.encoding import is_pkh
from pytezos.crypto import Key
from pytezos.rpc import mainnet


class OTP:

    def __init__(self, key, interval=5, shell=mainnet):
        """
        :param key: secret key (encrypted/unencrypted), public key or public key hash, all base58 encoded
        :param interval: number of blocks to check (tolerance)
        :param shell: ShellQuery instance
        """
        if not isinstance(key, Key):
            if is_pkh(key):
                key = shell.public_key(key)
            key = Key.from_encoded_key(key)

        self._key = key
        self._interval = interval
        self._shell = shell

    def now(self) -> str:
        if not self._key.secret_exponent:
            raise ValueError('Cannot generate OTP without a secret key')

        message = self._shell.head.calculate_hash()
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
