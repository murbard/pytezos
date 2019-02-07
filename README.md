# PyTezos

Python utils for Tezos.

## Requirements

* git
* python 3.6

## Installation

```
$ pip3 install git+https://github.com/baking-bad/pytezos --user
```

## Usage

```python

import pytezos

private_key = 'edsk3nM41ygNfSxVU4w1uAW3G9EnTQEB5rjojeZedLTGmiGRcierVv'

pytezos.Key(private_key).public_key()
>>> 'edpku976gpuAD2bXyx1XGraeKuCo1gUZ3LAJcHM12W1ecxZwoiu22R'

pytezos.Key(private_key).public_key_hash()
>>> 'tz1eKkWU5hGtfLUiqNpucHrXymm83z3DG9Sq'

pytezos.Key(private_key).sign('test')
>>> 'edsigtzLBGCyadERX1QsYHKpwnxSxEYQeGLnJGsSkHEsyY8vB5GcNdnvzUZDdFevJK7YZQ2ujwVjvQZn62ahCEcy74AwtbA8HuN'

public_key = 'edpku976gpuAD2bXyx1XGraeKuCo1gUZ3LAJcHM12W1ecxZwoiu22R'
signature = 'edsigtzLBGCyadERX1QsYHKpwnxSxEYQeGLnJGsSkHEsyY8vB5GcNdnvzUZDdFevJK7YZQ2ujwVjvQZn62ahCEcy74AwtbA8HuN'

pytezos.Key(public_key).verify(signature, 'fake')
>>> Exception('Signature is not valid.')
```

## Supported elliptic curves

* Ed25519 (tz1)
* SECP256k1 (tz2)

P256 signatures (tz3) will be implemented soon.

## Troubleshooting

* If you get ```command 'gcc' failed with exit status 1``` while installing secp256k1 package, it's probably system libraries issue: https://github.com/ludbb/secp256k1-py#installation-with-compilation