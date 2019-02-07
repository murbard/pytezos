from unittest import TestCase
from parameterized import parameterized

from pytezos import Key


class TestPyTezos(TestCase):
    """
    Test data generation:
    ./tezos-client gen keys test_ed25519 -s ed25519 --force
    ./tezos-client gen keys test_secp256k1 -s secp256k1 --force
    ./tezos-client gen keys test_p256 -s p256 --force
    ./tezos-client show address test_ed25519 -S
    ./tezos-client show address test_secp256k1 -S
    ./tezos-client show address test_p256 -S
    ./tezos-client sign bytes 0x74657374 for test_ed25519
    ./tezos-client sign bytes 0x74657374 for test_secp256k1
    ./tezos-client sign bytes 0x74657374 for test_p256
    """

    @parameterized.expand([
        ('edsk3nM41ygNfSxVU4w1uAW3G9EnTQEB5rjojeZedLTGmiGRcierVv',
         'edpku976gpuAD2bXyx1XGraeKuCo1gUZ3LAJcHM12W1ecxZwoiu22R',
         'tz1eKkWU5hGtfLUiqNpucHrXymm83z3DG9Sq'),
        ('spsk1zkqrmst1yg2c4xi3crWcZPqgdc9KtPtb9SAZWYHAdiQzdHy7j',
         'sppk7aMNM3xh14haqEyaxNjSt7hXanCDyoWtRcxF8wbtya859ak6yZT',
         'tz28YZoayJjVz2bRgGeVjxE8NonMiJ3r2Wdu'),
        # ('p2sk3PM77YMR99AvD3fSSxeLChMdiQ6kkEzqoPuSwQqhPsh29irGLC',
        #  'p2pk679D18uQNkdjpRxuBXL5CqcDKTKzsiXVtc9oCUT6xb82zQmgUks',
        #  'tz3agP9LGe2cXmKQyYn6T68BHKjjktDbbSWX')
    ])
    def test_derive_key_data(self, sk, pk, hash):
        public_key = Key(pk)
        self.assertFalse(public_key.is_secret)
        self.assertEqual(pk, public_key.public_key())
        self.assertEqual(hash, public_key.public_key_hash())

        secret_key = Key(sk)
        self.assertTrue(secret_key.is_secret)
        self.assertEqual(sk, secret_key.secret_key())
        self.assertEqual(pk, secret_key.public_key())

    @parameterized.expand([
        ('edpku976gpuAD2bXyx1XGraeKuCo1gUZ3LAJcHM12W1ecxZwoiu22R',
         b'test',
         'edsigtzLBGCyadERX1QsYHKpwnxSxEYQeGLnJGsSkHEsyY8vB5GcNdnvzUZDdFevJK7YZQ2ujwVjvQZn62ahCEcy74AwtbA8HuN'),
        ('sppk7aMNM3xh14haqEyaxNjSt7hXanCDyoWtRcxF8wbtya859ak6yZT',
         b'test',
         'spsig1RriZtYADyRhyNoQMa6AiPuJJ7AUDcrxWZfgqexzgANqMv4nXs6qsXDoXcoChBgmCcn2t7Y3EkJaVRuAmNh2cDDxWTdmsz')
    ])
    def test_verify_ext_signatures(self, pk, msg, sig):
        key = Key(pk)
        key.verify(sig, msg)
        self.assertRaises(Exception, key.verify, sig, b'fake')

    @parameterized.expand([
        ('edsk3nM41ygNfSxVU4w1uAW3G9EnTQEB5rjojeZedLTGmiGRcierVv', '0xdeadbeaf'),
        ('spsk1zkqrmst1yg2c4xi3crWcZPqgdc9KtPtb9SAZWYHAdiQzdHy7j', b'hello')
    ])
    def test_sign_and_verify(self, sk, msg):
        key = Key(sk)
        sig = key.sign(msg)
        key.verify(sig, msg)

    @parameterized.expand([
        ('edsk3nM41ygNfSxVU4w1uAW3G9EnTQEB5rjojeZedLTGmiGRcierVv',
         b'test',
         'edsigtzLBGCyadERX1QsYHKpwnxSxEYQeGLnJGsSkHEsyY8vB5GcNdnvzUZDdFevJK7YZQ2ujwVjvQZn62ahCEcy74AwtbA8HuN'),
        ('spsk1zkqrmst1yg2c4xi3crWcZPqgdc9KtPtb9SAZWYHAdiQzdHy7j',
         b'test',
         'spsig1RriZtYADyRhyNoQMa6AiPuJJ7AUDcrxWZfgqexzgANqMv4nXs6qsXDoXcoChBgmCcn2t7Y3EkJaVRuAmNh2cDDxWTdmsz'),
    ])
    def test_deterministic_signatures(self, sk, msg, sig):
        """
        See RFC6979 for explanation
        https://tools.ietf.org/html/rfc6979#section-3.2
        """
        key = Key(sk)
        signature = key.sign(msg)
        self.assertEqual(sig, signature)
