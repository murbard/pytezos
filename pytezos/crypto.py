import hashlib
import pysodium
import secp256k1
import unicodedata
from fastecdsa.ecdsa import sign, verify
from fastecdsa.keys import get_public_key
from fastecdsa.curve import P256
from fastecdsa.encoding.util import int_to_bytes, bytes_to_int
from fastecdsa.encoding.sec1 import SEC1Encoder
from pyblake2 import blake2b

from pytezos.encoding import scrub_input, base58_decode, base58_encode


def blake2b_32(v=b''):
    return blake2b(scrub_input(v), digest_size=32)


class Key(object):
    """
    Represents a public or secret key for Tezos. Ed25519, Secp256k1 and P256
    are supported.
    """
    def __init__(self, key: str, passphrase: str = None, email: str = None):
        """
        Creates a key object from a base58 encoded key.
        :param key: a public or secret key in base58 encoding, or a 15 word bip39 english mnemonic
        :param passphrase: the passphrase used if the key provided is an encrypted private key or a fundraiser key
        :param email: email used if a fundraiser key is passed
        """
        key = scrub_input(key)

        if email:
            if not passphrase:
                raise Exception("Fundraiser key provided without a passphrase.")

            mnemonic = u' '.join(key).lower()
            passphrase = scrub_input(passphrase)
            # TODO check wordlist and checksum
            salt = unicodedata.normalize(
                "NFKD", (email + passphrase).decode("utf8")).encode("utf8")
            seed = hashlib.pbkdf2_hmac("sha512", mnemonic, "mnemonic" + salt, iterations=2048, dklen=64)

            self._public_key, self._secret_key = pysodium.crypto_sign_seed_keypair(seed[:32])
            self.curve = b"ed"
            self.is_secret = True
            del passphrase
            return

        self.curve = key[:2]  # "sp", "p2" "ed"
        if self.curve not in [b"sp", b"p2", b"ed"]:
            raise ValueError("Invalid prefix for a key encoding.")

        if not len(key) in [54, 55, 88, 98]:
            raise ValueError("Invalid length for a key encoding.")

        encrypted = (key[2:3] == b'e')

        public_or_secret = key[3:5] if encrypted else key[2:4]
        if public_or_secret not in [b"pk", b"sk"]:
            raise Exception("Invalid prefix for a key encoding.")

        self.is_secret = (public_or_secret == b"sk")

        key = base58_decode(key)

        if encrypted:
            if not passphrase:
                raise ValueError("Encrypted key provided without a passphrase.")

            salt, encrypted_sk = key[:8], key[8:]
            encryption_key = hashlib.pbkdf2_hmac(
                hash_name="sha512",
                password=scrub_input(passphrase),
                salt=salt,
                iterations=32768,
                dklen=32
            )
            key = pysodium.crypto_secretbox_open(
                c=encrypted_sk, nonce=b'\000' * 24, k=encryption_key)
            del passphrase

        if not self.is_secret:
            self._public_key = key
            self._secret_key = None
        else:
            self._secret_key = key
            # Ed25519
            if self.curve == b"ed":
                # Dealing with secret key or seed?
                if len(key) == 64:
                    self._public_key = pysodium.crypto_sign_sk_to_pk(sk=key)
                else:
                    self._public_key, self._secret_key = pysodium.crypto_sign_seed_keypair(seed=key)
            # Secp256k1
            elif self.curve == b"sp":
                sk = secp256k1.PrivateKey(key)
                self._public_key = sk.pubkey.serialize()
            # P256
            elif self.curve == b"p2":
                pk = get_public_key(bytes_to_int(self._secret_key), curve=P256)
                self._public_key = SEC1Encoder.encode_public_key(pk)
            else:
                assert False

    def public_key(self):
        """
        :return: the public key associated with the private key
        """
        return base58_encode(self._public_key, self.curve + b'pk').decode()

    def secret_key(self, passphrase=None):
        """
        :param passphrase: encryption phrase for the private key
        :return: the secret key associated with this key, if available
        """
        if not self._secret_key:
            raise ValueError("Secret key not known.")

        if self.curve == b'ed':
            key = pysodium.crypto_sign_sk_to_seed(self._secret_key)
        else:
            key = self._secret_key

        if passphrase:
            salt = pysodium.randombytes(8)
            encryption_key = hashlib.pbkdf2_hmac(
                hash_name="sha512",
                password=scrub_input(passphrase),
                salt=salt,
                iterations=32768,
                dklen=32
            )
            encrypted_sk = pysodium.crypto_secretbox(
                msg=key, nonce=b'\000' * 24, k=encryption_key)
            key = salt + encrypted_sk  # we have to combine salt and encrypted key in order to decrypt later
            prefix = self.curve + b'esk'
        else:
            prefix = self.curve + b'sk'

        return base58_encode(key, prefix).decode()

    def public_key_hash(self):
        """
        Public key hash for this key.
        :return: the public key hash for this key
        """
        pkh = blake2b(data=self._public_key, digest_size=20).digest()
        prefix = {b'ed': b'tz1', b'sp': b'tz2', b'p2': b'tz3'}[self.curve]
        return base58_encode(pkh, prefix).decode()

    def sign(self, message, generic=False):
        """
        Sign a raw sequence of bytes
        :param message: sequence of bytes, raw format or hexadecimal notation
        :param generic: do not specify elliptic curve if set to True
        :return: signature in base58 encoding
        """
        message = scrub_input(message)

        if not self.is_secret:
            raise ValueError("Cannot sign without a secret key.")

        # Ed25519
        if self.curve == b"ed":
            digest = pysodium.crypto_generichash(message)
            signature = pysodium.crypto_sign_detached(digest, self._secret_key)
        # Secp256k1
        elif self.curve == b"sp":
            pk = secp256k1.PrivateKey(self._secret_key)
            signature = pk.ecdsa_serialize_compact(
                pk.ecdsa_sign(message, digest=blake2b_32))
        # P256
        elif self.curve == b"p2":
            r, s = sign(msg=message, d=bytes_to_int(self._secret_key), hashfunc=blake2b_32)
            signature = int_to_bytes(r) + int_to_bytes(s)
        else:
            assert False

        if generic:
            prefix = b'sig'
        else:
            prefix = self.curve + b'sig'

        return base58_encode(signature, prefix).decode()

    def verify(self, signature, message):
        """
        Verify signature, raise exception if it is not valid
        :param message: sequance of bytes, raw format or hexadecimal notation
        :param signature: a signature in base58 encoding
        """
        signature = scrub_input(signature)
        message = scrub_input(message)

        if not self._public_key:
            raise ValueError("Cannot verify without a public key")

        if signature[:3] != b'sig':  # not generic
            if self.curve != signature[:2]:  # "sp", "p2" "ed"
                raise ValueError("Signature and public key curves mismatch.")

        signature = base58_decode(signature)

        # Ed25519
        if self.curve == b"ed":
            digest = pysodium.crypto_generichash(message)
            try:
                pysodium.crypto_sign_verify_detached(signature, digest, self._public_key)
            except ValueError:
                raise ValueError('Signature is invalid.')
        # Secp256k1
        elif self.curve == b"sp":
            pk = secp256k1.PublicKey(self._public_key, raw=True)
            sig = pk.ecdsa_deserialize_compact(signature)
            if not pk.ecdsa_verify(message, sig, digest=blake2b_32):
                raise ValueError('Signature is invalid.')
        # P256
        elif self.curve == b"p2":
            pk = SEC1Encoder.decode_public_key(self._public_key, curve=P256)
            r, s = bytes_to_int(signature[:32]), bytes_to_int(signature[32:])
            if not verify(sig=(r, s), msg=message, Q=pk, hashfunc=blake2b_32):
                raise ValueError('Signature is invalid.')
        else:
            assert False
