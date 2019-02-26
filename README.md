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

### RPC: query builder and a little bit more

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

There are also some syntax sugar for convenient collection iteration:

```python
mainnet.blocks[329830:329836]
>>> [['BLiZM5t1cQSDde9Acv4JGYNetA3rS6tAEinvkwYhaFvMvsQE9XB',
  'BLZ1R83AHKknKzmNPqF22aMYL6jQcPU1EBQ8W1PagV3ag6pysWQ',
  'BLXCMEHUpHtwB1RoFGnzVnoVf7FEmeEwz8Ad5dxtrRcq5tD3DeB',
  'BLVrBJyGdm9j4su7exVtkTNi4aJ1D9ephUfPfZFzZwGoRDc8T5z',
  'BLuNPrD4QxjBWc26eDnuoCg7qFSutVURoZpToHshLbbuhZBsb5X',
  'BKujfxvZvqrVmz4anJz6JNQgKe5w7sudcb7awBKUYY39XhReMQp']]

mainnet.blocks[-2:]
>>> [['BKkAhaDbzaFEm99wWedeELxzXHrozQrG4B4p8BU56ttmDjsMdge',
  'BL8u6Ny9naUnVWAtNJQ4P93LfgW8x9LDUCGoW9TEEzqHiG4mPsu']]
```

And several methods for operations manipulation:

```python
ops = mainnet.mempool.pending_operations.applied(kind='endorsement')

ops[0].forge()
>>> '6b96a5df309727b4cd9a2aee24a56a83565db00d7dce158d5b55400d92f5022c0000050888'

ops[0].preapply()
>>> [{'contents': [{'kind': 'endorsement',
    'level': 329864,
    'metadata': {'balance_updates': [{'kind': 'contract',
       'contract': 'tz3RDC3Jdn4j15J7bBHZd29EUee9gVB1CxD9',
       'change': '-128000000'},
      {'kind': 'freezer',
       'category': 'deposits',
       'delegate': 'tz3RDC3Jdn4j15J7bBHZd29EUee9gVB1CxD9',
       'level': 80,
       'change': '128000000'},
      {'kind': 'freezer',
       'category': 'rewards',
       'delegate': 'tz3RDC3Jdn4j15J7bBHZd29EUee9gVB1CxD9',
       'level': 80,
       'change': '4000000'}],
     'delegate': 'tz3RDC3Jdn4j15J7bBHZd29EUee9gVB1CxD9',
     'slots': [15, 5]}}],
  'signature': 'sigsfBsrxKVcS8btuik6vgqR1TRNundZD36ph2tEgjUQdMqHjrNYziJ6godapYMCKq483XqS7rcvfPD61StZ63TE5Jchujs4'}]

ops[0].verify_signature()
>>> No exceptions
```

The best thing about this wrapper is that you can use not yet wrapped RPC endpoints:

```python
mainnet.context.delegates(active=True)
>>> ['tz2KuCcKSyMzs8wRJXzjqoHgojPkSUem8ZBS',
 'tz2JMPu9yVKuX2Au8UUbp7YrKBZJSdYhgwwu',
 'tz2E3BvcMiGvFEgNVdsAiwVvPHcwJDTA8wLt', ... ]
```

Or just use raw requests:

```python
from pytezos.rpc.node import Node

node = Node()
node.get('chains/main/blocks', params={'length': 1})
>>> [['BKvRWnbPeFzFNJ9mkUEcxCzYk68fLa3mPYweqcFVo7TNLAJAz2G'], ... ]

node.post('chains/main/mempool/filter', json={'minimal_fees': 0})
>>> {}
```

