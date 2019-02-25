# PyTezos

[![Build Status](https://travis-ci.org/baking-bad/pytezos.svg?branch=master)](https://travis-ci.org/baking-bad/pytezos)
[![Made With](https://img.shields.io/badge/made%20with-python-blue.svg?)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python utils for Tezos.

## Requirements

* git
* python 3.6+ (can't resist string interpolation)
* pip 19.0.1+ (in order to support poetry packages)

You will also probably need to install several cryptographic packets:

```
$ sudo apt install libsodium-dev libsecp256k1-dev libgmp-dev
```

## Installation

```
$ pip install git+https://github.com/baking-bad/pytezos
```

## Usage

### Crypto: keys and signatures

All the three elliptic curves are now supported: ed25519, secp256k1, p256 (secp256r1).

```python
from pytezos.crypto import Key

private_key = 'edsk3nM41ygNfSxVU4w1uAW3G9EnTQEB5rjojeZedLTGmiGRcierVv'

Key(private_key).public_key()
>>> 'edpku976gpuAD2bXyx1XGraeKuCo1gUZ3LAJcHM12W1ecxZwoiu22R'

Key(private_key).public_key_hash()
>>> 'tz1eKkWU5hGtfLUiqNpucHrXymm83z3DG9Sq'

Key(private_key).sign('test')
>>> 'edsigtzLBGCyadERX1QsYHKpwnxSxEYQeGLnJGsSkHEsyY8vB5GcNdnvzUZDdFevJK7YZQ2ujwVjvQZn62ahCEcy74AwtbA8HuN'

public_key = 'edpku976gpuAD2bXyx1XGraeKuCo1gUZ3LAJcHM12W1ecxZwoiu22R'
signature = 'edsigtzLBGCyadERX1QsYHKpwnxSxEYQeGLnJGsSkHEsyY8vB5GcNdnvzUZDdFevJK7YZQ2ujwVjvQZn62ahCEcy74AwtbA8HuN'

Key(public_key).verify(signature, 'fake')
>>> Exception('Signature is not valid.')
```

### RPC: a query builder and a little bit more

Tezos node API was designed with REST in mind and this package reflects it as well. Basically it's a query building machine, like sqlalchemy for SQL. In addition to this functional it also offers smart caching, shortcuts, and autocomplete, which is very helpful for doing researches in jupyter notebook for instance.

```python
from pytezos.rpc import mainnet

mainnet.head.hash
>>> chains/main/blocks/head/hash

mainnet.head.hash()
>>> 'BKiWhfLw4Qc49pzimVZkvUW5UKbhcbEDNc8UXsbuLsztu92RG8U'

mainnet.blocks(length=2, head='BLyvi5G4i6zaqLPL2r1k2SLKwQp8tsYXEf4mAVrwRjF9w4qVVSv')
>>> [['BLyvi5G4i6zaqLPL2r1k2SLKwQp8tsYXEf4mAVrwRjF9w4qVVSv',
  'BKiWhfLw4Qc49pzimVZkvUW5UKbhcbEDNc8UXsbuLsztu92RG8U']]

mainnet.head.operations[0, 0]
>>> chains/main/blocks/head/operations/0/0

mainnet.context.contracts['tz1TNWtofRofCU11YwCNwTMWNFBodYi6eNqU']()
>>> {'manager': 'tz1TNWtofRofCU11YwCNwTMWNFBodYi6eNqU',
 'balance': '384854285987',
 'spendable': True,
 'delegate': {'setable': False,
  'value': 'tz1TNWtofRofCU11YwCNwTMWNFBodYi6eNqU'},
 'counter': '2317'}
```

It's cool, but what about POST/PUT/DELETE requests? This is the best part: 
