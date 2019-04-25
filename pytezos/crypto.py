import hashlib
import pysodium
import secp256k1
import binascii
from fastecdsa.ecdsa import sign, verify
from fastecdsa.keys import get_public_key
from fastecdsa.curve import P256
from fastecdsa.encoding.util import int_to_bytes, bytes_to_int
from fastecdsa.encoding.sec1 import SEC1Encoder
from pyblake2 import blake2b
from mnemonic import Mnemonic

from pytezos.encoding import scrub_input, base58_decode, base58_encode


def blake2b_32(v=b''):
    return blake2b(scrub_input(v), digest_size=32)


def validate_mnemonic(mnemonic, language='english'):
    m = Mnemonic(language)
    mnemonic = m.normalize_string(mnemonic).split(' ')
    if len(mnemonic) not in [12, 15, 18, 21, 24]:
        raise ValueError(
            'Number of words must be one of the following: [12, 15, 18, 21, 24], but it is not (%d).' % len(mnemonic))

    idx = map(lambda x: bin(m.wordlist.index(x))[2:].zfill(11), mnemonic)
    b = ''.join(idx)
    l = len(b)
    d = b[:l // 33 * 32]
    h = b[-l // 33:]
    nd = binascii.unhexlify(hex(int(d, 2))[2:].rstrip('L').zfill(l // 33 * 8))
    nh = bin(int(hashlib.sha256(nd).hexdigest(), 16))[2:].zfill(256)[:l // 33]
    if h != nh:
        raise ValueError('Failed checksum.')


class Key(object):
    """
    Represents a public or secret key for Tezos. Ed25519, Secp256k1 and P256
    are supported.
    """
    def __init__(self, public_key, secret_key=None, curve=b'ed'):
        self._public_key = public_key
        self._secret_key = secret_key
        self.curve = curve
        self.is_secret = secret_key is not None

    @classmethod
    def from_secret_key(cls, secret_key: bytes, curve=b'ed'):
        """
        Creates a key object from a secret exponent.
        :param secret_key: secret exponent or seed
        :param curve: an elliptic curve used, default is ed25519
        """
        # Ed25519
        if curve == b'ed':
            # Dealing with secret key or seed?
            if len(secret_key) == 64:
                public_key = pysodium.crypto_sign_sk_to_pk(sk=secret_key)
            else:
                public_key, secret_key = pysodium.crypto_sign_seed_keypair(seed=secret_key)
        # Secp256k1
        elif curve == b'sp':
            sk = secp256k1.PrivateKey(secret_key)
            public_key = sk.pubkey.serialize()
        # P256
        elif curve == b'p2':
            pk = get_public_key(bytes_to_int(secret_key), curve=P256)
            public_key = SEC1Encoder.encode_public_key(pk)
        else:
            assert False

        return cls(public_key, secret_key, curve=curve)

    @classmethod
    def from_public_key(cls, public_key: bytes, curve=b'ed'):
        """
        Creates a key object from a public elliptic point.
        :param public_key: elliptic point in the compressed format (see https://tezos.stackexchange.com/a/623/309)
        :param curve: an elliptic curve used, default is ed25519
        """
        return cls(public_key, curve=curve)

    @classmethod
    def from_key(cls, key, passphrase=''):
        """
        Creates a key object from a base58 encoded key.
        :param key: a public or secret key in base58 encoding
        :param passphrase: the passphrase used if the key provided is an encrypted private key
        """
        key = scrub_input(key)

        curve = key[:2]  # "sp", "p2" "ed"
        if curve not in [b"sp", b"p2", b"ed"]:
            raise ValueError("Invalid prefix for a key encoding.")
        if not len(key) in [54, 55, 88, 98]:
            raise ValueError("Invalid length for a key encoding.")

        encrypted = (key[2:3] == b'e')
        public_or_secret = key[3:5] if encrypted else key[2:4]
        if public_or_secret not in [b"pk", b"sk"]:
            raise Exception("Invalid prefix for a key encoding.")

        key = base58_decode(key)
        is_secret = (public_or_secret == b"sk")
        if not is_secret:
            return cls.from_public_key(key, curve)

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

        return cls.from_secret_key(key, curve)

    @classmethod
    def from_mnemonic(cls, mnemonic, passphrase='', email='', validate=True):
        """
        Creates a key object from a bip39 mnemonic.
        :param mnemonic: a 15 word bip39 english mnemonic
        :param passphrase: a mnemonic password or a fundraiser key
        :param email: email used if a fundraiser key is passed
        :param validate: whether to check mnemonic or not
        """
        if isinstance(mnemonic, list):
            mnemonic = ' '.join(mnemonic)

        if validate:
            validate_mnemonic(mnemonic)

        seed = Mnemonic.to_seed(mnemonic, passphrase=email + passphrase)
        public_key, secret_key = pysodium.crypto_sign_seed_keypair(seed=seed[:32])
        return cls(public_key, secret_key)

    def public_key(self):
        """
        Creates base58 encoded public key representation
        :return: the public key associated with the private key
        """
        return base58_encode(self._public_key, self.curve + b'pk').decode()

    def secret_key(self, passphrase=None):
        """
        Creates base58 encoded private key representation
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
        Creates base58 encoded public key hash for this key.
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
