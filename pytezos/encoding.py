import base58


def tb(l):
    return b''.join(map(lambda x: x.to_bytes(1, 'big'), l))


base58_encodings = [
    # encoded prefix | encoded length | decoded prefix | data type
    (b"B", 51, tb([1, 52]), u"block hash"),
    (b"o", 51, tb([5, 116]), u"operation hash"),
    (b"Lo", 52, tb([133, 233]), u"operation list hash"),
    (b"LLo", 53, tb([29, 159, 109]), u"operation list list hash"),
    (b"P", 51, tb([2, 170]), u"protocol hash"),
    (b"Co", 52, tb([79, 199]), u"context hash"),
    (b"tz1", 36, tb([6, 161, 159]), u"ed25519 public key hash"),
    (b"tz2", 36, tb([6, 161, 161]), u"secp256k1 public key hash"),
    (b"tz3", 36, tb([6, 161, 164]), u"p256 public key hash"),
    (b"edpk", 54, tb([13, 15, 37, 217]), u"ed25519 public key"),
    (b"sppk", 55, tb([3, 254, 226, 86]), u"secp256k1 public key"),
    (b"p2pk", 55, tb([3, 178, 139, 127]), u"p256 public key"),
    (b"edsk", 54, tb([13, 15, 58, 7]), u"ed25519 seed"),
    (b"spsk", 54, tb([17, 162, 224, 201]), u"secp256k1 secret key"),
    (b"p2sk", 54, tb([16, 81, 238, 189]), u"p256 secret key"),
    (b"edesk", 88, tb([7, 90, 60, 179, 41]), u"ed25519 encrypted seed"),
    (b"spesk", 88, tb([9, 237, 241, 174, 150]), u"secp256k1 encrypted secret key"),
    (b"p2esk", 88, tb([9, 48, 57, 115, 171]), u"p256_encrypted_secret_key"),
    (b"edsk", 98, tb([43, 246, 78, 7]), u"ed25519 secret key"),
    (b"edsig", 99, tb([9, 245, 205, 134, 18]), u"ed25519 signature"),
    (b"spsig", 99, tb([13, 115, 101, 19, 63]), u"secp256k1 signature"),
    (b"p2sig", 98, tb([54, 240, 44, 52]), u"p256 signature"),
    (b"sig", 96, tb([4, 130, 43]), u"generic signature")
]


def scrub_input(v) -> bytes:
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


def base58_decode(v: bytes) -> bytes:
    try:
        prefix_len = next(
            len(encoding[2])
            for encoding in base58_encodings
            if len(v) == encoding[1] and v.startswith(encoding[0])
        )
    except StopIteration:
        raise ValueError('Invalid encoding, prefix or length mismatch.')

    return base58.b58decode_check(v)[prefix_len:]


def base58_encode(v: bytes, prefix: bytes) -> bytes:
    try:
        encoding = next(
            encoding
            for encoding in base58_encodings
            if prefix == encoding[0]
        )
    except StopIteration:
        raise ValueError('Invalid encoding prefix.')

    return base58.b58encode_check(encoding[2] + v)
