import hashlib
import pysodium
from pyblake2 import blake2b
import base58
import secp256k1
import unicodedata


def tb(l):
    return b''.join(map(lambda x: x.to_bytes(1, 'big'), l))


def scrub_input(v):
    if isinstance(v, str) and not isinstance(v, bytes):
        if v.startswith('0x'):
            v = bytes.fromhex(v[2:])
        else:
            v = v.encode('ascii')

    if not isinstance(v, bytes):
        raise TypeError(
            "a bytes-like object is required (also str), not '%s'" %
            type(v).__name__)

    return v


b58_encodings = {
    (b"tz1",   36): (tb([6,  161, 159]),           u"ed25519 public key hash"),
    (b"tz2",   36): (tb([6,  161, 161]),           u"secp256k1 public key hash"),
    (b"tz3",   36): (tb([6,  161, 164]),           u"p256 public key hash"),
    (b"edpk",  54): (tb([13, 15,  37,  217]),      u"ed25519 public key"),
    (b"sppk",  55): (tb([3,  254, 226, 86]),       u"secp256k1 public key"),
    (b"p2pk",  55): (tb([3,  178, 139, 127]),      u"p256 public key"),
    (b"edsk",  54): (tb([13, 15,  58,  7]),        u"ed25519 seed"),
    (b"spsk",  54): (tb([17, 162, 224, 201]),      u"secp256k1 secret key"),
    (b"p2sk",  54): (tb([16, 81,  238, 189]),      u"p256 secret key"),
    (b"edesk", 88): (tb([7,  90,  60,  179, 41]),  u"ed25519 encrypted seed"),
    (b"spesk", 88): (tb([9,  237, 241, 174, 150]), u"secp256k1 encrypted secret key"),
    (b"p2esk", 88): (tb([9,  48,  57,  115, 171]), u"p256_encrypted_secret_key"),
    (b"edsk",  98): (tb([43, 246, 78,  7]),        u"ed25519 secret key"),
    (b"edsig", 99): (tb([9,  245, 205, 134, 18]),  u"ed25519 signature"),
    (b"spsig", 99): (tb([13, 115, 101, 19,  63]),  u"secp256k1 signature"),
    (b"p2sig", 98): (tb([54, 240, 44,  52]),       u"p256 signature"),
    (b"sig",   96): (tb([4,  130, 43]),            u"generic signature")
}


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
        if passphrase:
            passphrase = scrub_input(passphrase)

        if email is not None:
            mnemonic = u' '.join(key).lower()
            # TODO check wordlist and checksum
            salt = unicodedata.normalize(
                "NFKD", (email + passphrase).decode("utf8")).encode("utf8")

            seed = hashlib.pbkdf2_hmac("sha512", mnemonic, "mnemonic" + salt, 2048, 64)
            self._public_key, self._secret_key = pysodium.crypto_sign_seed_keypair(seed[0:32])
            self.curve = b"ed"
            self.is_secret = True
            return

        self.curve = key[:2]  # "sp", "p2" "ed"
        if self.curve not in [b"sp", b"p2", b"ed"]:
            raise Exception("Invalid prefix for a key encoding.")

        if not len(key) in [54, 55, 88, 98]:
            raise Exception("Invalid length for a key encoding.")

        encrypted = (key[2:3] == b'e')

        public_or_secret = key[3:5] if encrypted else key[2:4]
        if public_or_secret not in [b"pk", b"sk"]:
            raise Exception("Invalid prefix for a key encoding.")

        self.is_secret = (public_or_secret == b"sk")

        encoding = (key[:5], len(key)) if encrypted else (key[:4], len(key))

        if encoding not in b58_encodings:
            raise Exception("Invalid encoding for a key, length or prefix mismatch.")

        key = base58.b58decode_check(key)[len(b58_encodings[encoding][0]):]

        if encrypted:
            if not passphrase:
                raise Exception("Encrypted key provided without passphrase.")
            key, salt = key[8:], key[:8]
            ek = hashlib.pbkdf2_hmac("sha512", passphrase, salt, 32768, 32)
            key = pysodium.crypto_secretbox_open(
                c=key, nonce=b'\000' * 24, k=ek)

        if not self.is_secret:
            self._public_key = key
            self._secret_key = None
        else:
            self._secret_key = key
            # Ed25519
            if self.curve == b"ed":
                # Dealing with secret key or seed?
                if encoding[1] == 98:
                    self._public_key = pysodium.crypto_sign_sk_to_pk(sk=key)
                else:
                    self._public_key, self._secret_key = pysodium.crypto_sign_seed_keypair(seed=key)
            # Secp256k1
            elif self.curve == b"sp":
                sk = secp256k1.PrivateKey(key)
                self._public_key = sk.pubkey.serialize()
            # P256
            elif self.curve == b"p2":
                raise Exception("Not implemented")
            else:
                assert False

    def public_key(self):
        """
        :return: the public key associated with the private key
        """
        prefix = b58_encodings[(self.curve + b'pk', 54 if self.curve == b'ed' else 55)][0]
        return base58.b58encode_check(prefix + self._public_key).decode()

    def secret_key(self, passphrase=None):
        """
        :param passphrase: encryption phrase for the private key
        :return: the secret key associated with this key, if available
        """
        if not self._secret_key:
            raise Exception("Secret key not known.")

        if self.curve == b'ed':
            key = pysodium.crypto_sign_sk_to_seed(self._secret_key)
        else:
            key = self._secret_key

        if passphrase:
            prefix = b58_encodings[(self.curve + b'esk', 88)][0]
            salt = pysodium.randombytes(8)
            ek = hashlib.pbkdf2_hmac("sha512", passphrase, salt, 32768, 32)
            key = pysodium.crypto_secretbox(msg=key, nonce=b'\000' * 24, k=ek)
        else:
            prefix = b58_encodings[(self.curve + b'sk', 54)][0]

        return base58.b58encode_check(prefix + key).decode()

    def public_key_hash(self):
        """
        Public key hash for this key.
        :return: the public key hash for this key
        """
        pkh = blake2b(data=self._public_key, digest_size=20).digest()
        prefix = b58_encodings[({b'ed': b'tz1', b'sp': b'tz2', b'p2': b'tz3'}[self.curve], 36)][0]
        return base58.b58encode_check(prefix + pkh).decode()

    def sign(self, message, generic=False):
        """
        Sign a raw sequence of bytes
        :param message: sequence of bytes, raw format or hexadecimal notation
        :param generic: do not specify elliptic curve if set to True
        :return: signature in base58 encoding
        """
        message = scrub_input(message)

        if not self.is_secret:
            raise Exception("Cannot sign without a secret key.")

        # Ed25519
        if self.curve == b"ed":
            digest = pysodium.crypto_generichash(message)
            signature = pysodium.crypto_sign_detached(digest, self._secret_key)
        # Secp256k1
        elif self.curve == b"sp":
            pk = secp256k1.PrivateKey(self._secret_key)
            signature = pk.ecdsa_serialize_compact(
                pk.ecdsa_sign(message, digest=lambda x: blake2b(x, digest_size=32)))
        # P256
        else:
            raise NotImplementedError(self.curve)

        if generic:
            encoding = (b'sig', 96)
        else:
            encoding = (self.curve + b'sig', 98 if self.curve == b"p2" else 99)

        prefix = b58_encodings[encoding][0]
        return base58.b58encode_check(prefix + signature).decode()

    def verify(self, signature, message):
        """
        Verify signature, raise exception if it is not valid
        :param message: sequance of bytes, raw format or hexadecimal notation
        :param signature: a signature in base58 encoding
        """
        signature = scrub_input(signature)
        message = scrub_input(message)

        if not self._public_key:
            raise Exception("Cannot verify without a public key")

        if signature[:3] == b'sig':
            is_generic = True
        else:
            is_generic = False
            if self.curve != signature[:2]:  # "sp", "p2" "ed"
                raise Exception("Signature and public key curves mismatch.")

        if not len(signature) in [99, 98, 96]:
            raise Exception("Invalid length for a signature encoding.")

        encoding = (signature[:3 if is_generic else 5], len(signature))
        if encoding not in b58_encodings:
            raise Exception("Invalid encoding for a signature, length or prefix mismatch.")

        signature = base58.b58decode_check(signature)[len(b58_encodings[encoding][0]):]

        # Ed25519
        if self.curve == b"ed":
            try:
                digest = pysodium.crypto_generichash(message)
                pysodium.crypto_sign_verify_detached(signature, digest, self._public_key)
            except ValueError:
                raise Exception('Signature is invalid.')
        # Secp256k1
        elif self.curve == b"sp":
            pk = secp256k1.PublicKey(self._public_key, raw=True)
            sig = pk.ecdsa_deserialize_compact(signature)
            if not pk.ecdsa_verify(
                    message, sig, digest=lambda x: blake2b(x, digest_size=32)):
                raise Exception('Signature is invalid.')
        # P256
        else:
            raise NotImplementedError(self.curve)
