## Introduction

PyTezos library is a Python toolset for Tezos blockchain, including work with keys, signatures, contracts, operations,
RPC query builder, and a high-level interface for smart contract interaction. It can be used to build a full-fledged
application, but also it's perfect for doing researches in Jupyter interactive notebooks.
In this quick start guide, we'll go through the main concepts and inspect one of the common use cases.

## Installation

First of all you'll probably need to install cryptographic libraries in your system.

Ubuntu:
```
$ sudo apt install libsodium-dev libsecp256k1-dev libgmp-dev
```

MacOS:
```
$ brew install libsodium
```

After that just install PyTezos from PyPi:
```
$ pip install pytezos
```

That's it! You can open Python console or Jupyter notebook and get to the next step.

## Set key and RPC node

All active interaction with the blockchain starts with the PyTezosClient:
```python
>>> from pytezos import pytezos
>>> pytezos
<pytezos.client.PyTezosClient object at 0x7f904cf339e8>

Key
tz1grSQDByRpnVs7sPtaprNZRp531ZKz6Jmm

Node
https://tezos-dev.cryptonomic-infra.tech/ (alphanet)

Helpers
.Contract()
.Key()
.Proto()
.account()
.activate_account()
.alphanet()
.ballot()
.contract()
.delegation()
.double_baking_evidence()
.double_endorsement_evidence()
.endorsement()
.mainnet()
.operation()
.operation_group()
.origination()
.proposals()
.reveal()
.seed_nonce_revelation()
.transaction()
.using()
.zeronet()
```

This is one of the cool features in the interactive mode: aside from the autocomplete and call docstrings,
you can see the list of available methods for class, or list of arguments and return value for a particular methods.
We are interested in `using` method, which is responsible for setting up manager key and RPC connection.
```python
>>> pytezos.using
<function Interop.using at 0x7fe5d2232840>

Change current rpc endpoint and account (private key)
:param shell: one of 'alphanet', 'mainnet', 'zeronet', RPC node uri, or instance of `ShellQuery`
:param key: base58 encoded key, path to the faucet file, alias from tezos-client, or instance of `Key`
:return: A copy of current object with changes applied
```

Note, that by default `pytezos` is initialized with `alphanet` and a predefined private key for demo purpose,
so you can start to interact immediately, but it's highly recommended to use your own key. Let's do that!

Go to the [https://faucet.tzalpha.net/](https://faucet.tzalpha.net/) and download key file.
Then configure the client (we can leave `shell` parameter empty, but we will set it explicitly for better understanding)
```python
>>> pytezos = pytezos.using(
...     key='~/Downloads/tz1cnQZXoznhduu4MVWfJF6GSyP6mMHMbbWa.json',
...     shell='https://rpc.tulip.tools/alphanet/')
```

Public available RPC providers are available at `pytezos.rpc`:
```python
>>> from pytezos.rpc import tulip
>>> tulip
<pytezos.rpc.RpcProvider object at 0x7f6f56ad77b8>

Networks
.mainnet  # https://rpc.tulip.tools/mainnet/
.alphanet  # https://rpc.tulip.tools/alphanet/
.zeronet  # https://rpc.tulip.tools/zeronet/
```

## Activate account

In order to start using our faucet account we need to claim balance.
```python
>>> pytezos.activate_account
<function ContentMixin.activate_account at 0x7f6f555e5400>

Activate recommended allocations for contributions to the TF fundraiser.
More info https://activate.tezos.com/
:param pkh: Public key hash, leave empty for autocomplete
:param activation_code: Secret code from pdf, leave empty for autocomplete
:return: dict or OperationGroup
```

Cool! We can just leave all fields empty and let PyTezos do all the work. There are two autocomplete function available:
`fill` and `autofill`. The only difference is that `autofill` simulates the operation and sets precise values for fee
and gas/storage limits.
```python
>>> pytezos.activate_account().autofill()
<pytezos.operation.group.OperationGroup object at 0x7f291b7074e0>

Key
tz1cnQZXoznhduu4MVWfJF6GSyP6mMHMbbWa

Node
https://rpc.tulip.tools/alphanet/ (alphanet)

Payload
{'branch': 'BL5UtKR4ysFLwcK2ign1h2KoZLJY88zd1vzWUZPzto9iEJqUj1d',
 'contents': [{'kind': 'activate_account',
               'pkh': 'tz1cnQZXoznhduu4MVWfJF6GSyP6mMHMbbWa',
               'secret': 'e8d47034af5ea23a9613dba219f8b4a792b22c5f'}],
 'protocol': 'Pt24m4xiPbLDhVgVfABUjirbmda3yohdN82Sp9FeuAXJ4eV9otd',
 'signature': None}

Helpers
.activate_account()
.autofill()
.ballot()
.binary_payload()
.delegation()
.double_baking_evidence()
.double_endorsement_evidence()
.endorsement()
.fill()
.forge()
.hash()
.inject()
.json_payload()
.operation()
.origination()
.preapply()
.proposals()
.reveal()
.run()
.seed_nonce_revelation()
.sign()
.transaction()
.using()
```

Have you noticed that operation helpers are still available? We can easily chain operations but we cannot for example
put `activate_account` and `reveal` together because they are from different validation passes.
Ok, let's sign and preapply operation to see what's going to happen:
```python
>>> pytezos.activate_account().fill().sign().preapply()
[{'contents': [{'kind': 'activate_account',
    'pkh': 'tz1cnQZXoznhduu4MVWfJF6GSyP6mMHMbbWa',
    'secret': 'e8d47034af5ea23a9613dba219f8b4a792b22c5f',
    'metadata': {'balance_updates': [{'kind': 'contract',
       'contract': 'tz1cnQZXoznhduu4MVWfJF6GSyP6mMHMbbWa',
       'change': '10848740286'}]}}],
  'signature': 'sigRg96wY6mxLKJ7jaTrVcXzABqhyEa4J1Ji5rGPKPVHv2YugViGfeH1b7qu7eavhhEGoASqffwjnH2fr46oBXVZrMWC6ZFg'}]
```

Everything looks good! Ready to inject the operation.
```python
>>> pytezos.activate_account().fill().sign().inject()
'oo77zoEsa9RuA7NubhvckM8NBNta8dUbL4e5GuhXmqnZ9XQGK5k'
```

We can search our operation in the node mempool to check what status it has:
```python
>>> pytezos.shell.mempool.pending_operations['oo77zoEsa9RuA7NubhvckM8NBNta8dUbL4e5GuhXmqnZ9XQGK5k']
{'status': 'applied',
 'hash': 'oo77zoEsa9RuA7NubhvckM8NBNta8dUbL4e5GuhXmqnZ9XQGK5k',
 'branch': 'BMdgSQxnGGTXuvGp7qrgnM2pMu16dS9Hdjq9UbdHGxzxfKfVR75',
 'contents': [{'kind': 'activate_account',
   'pkh': 'tz1cnQZXoznhduu4MVWfJF6GSyP6mMHMbbWa',
   'secret': 'e8d47034af5ea23a9613dba219f8b4a792b22c5f'}],
 'signature': 'sigbMMUu6h9vAxoM7ZZdwttDk2CcgpwbmCrFjSTQBtTsoLFYNdz85wCKQBMZ2ZMEVrBnt61XGZXyWuuDDbp7WepjHgR6DTrT'}

>>> pytezos.account()
{'manager': 'tz1cnQZXoznhduu4MVWfJF6GSyP6mMHMbbWa',
 'balance': '10848740286',
 'spendable': True,
 'delegate': {'setable': False},
 'counter': '715917'}
```

Yay! We have claimed our account balance.

## Reveal public key

```python
>>> pytezos.reveal().autofill().sign().inject()
'oo3TzPdNhtz5nmE9nL2yGLqwUzSfmb1vjTpu8wFkX5CTKLV67AE'
```

We can also search for operation by hash if we know exact block level or that it was injected recently:
```python
>>> pytezos.shell.blocks[580244].operations['oo3TzPdNhtz5nmE9nL2yGLqwUzSfmb1vjTpu8wFkX5CTKLV67AE']
<pytezos.rpc.protocol.OperationQuery object at 0x7f70650925c0>

Path
/chains/main/blocks/580244/operations/3/16

()
The `m-th` operation in the `n-th` validation pass of the block.
:return: Object

Helpers
.unsigned()

>>> pytezos.shell.blocks[-20:].find_operation('oo3TzPdNhtz5nmE9nL2yGLqwUzSfmb1vjTpu8wFkX5CTKLV67AE')
{'protocol': 'Pt24m4xiPbLDhVgVfABUjirbmda3yohdN82Sp9FeuAXJ4eV9otd',
 'chain_id': 'NetXgtSLGNJvNye',
 'hash': 'oo3TzPdNhtz5nmE9nL2yGLqwUzSfmb1vjTpu8wFkX5CTKLV67AE',
 'branch': 'BLdKQLeV5FaPspBLP6J7Tx5xs2XRRH7pJGnXhwEW1uKz9PGBF8H',
 'contents': [{'kind': 'reveal',
   'source': 'tz1cnQZXoznhduu4MVWfJF6GSyP6mMHMbbWa',
   'fee': '1261',
   'counter': '715918',
   'gas_limit': '10000',
   'storage_limit': '0',
   'public_key': 'edpktn9Xg5TaBJ9j6gs1X4AAsQR43zxzmaVNdyerq2PxTy7dUfN3X8',
   'metadata': {'balance_updates': [{'kind': 'contract',
      'contract': 'tz1cnQZXoznhduu4MVWfJF6GSyP6mMHMbbWa',
      'change': '-1261'},
     {'kind': 'freezer',
      'category': 'fees',
      'delegate': 'tz3gN8NTLNLJg5KRsUU47NHNVHbdhcFXjjaB',
      'cycle': 283,
      'change': '1261'}],
    'operation_result': {'status': 'applied', 'consumed_gas': '10000'}}}],
 'signature': 'sigjzUVPWuFKxmMizHfMUgjqXpo2cqNEHjgRDykqwWiot2129KRWCanZjytUfxFWSDwpNSjkakmWqzhxLwNNcBcQQWJ5mAsW'}
```

## Originate contract

Now we can do something interesting. Let's deploy a Michelson smart contract! First we need to load data, in this
tutorial we will get it from Michelson source file. There are plenty of available methods, but we'are interested in
`script` which gives us payload for origination.
```python
>>> from pytezos import Contract
>>> contract = Contract.from_file('~/Documents/demo_contract.tz')
>>> contract.script
<function Contract.script at 0x7fe01c0d9c80>

Generate script for contract origination
:param storage: Python object, leave None to generate empty
:return: {"code": $Micheline, "storage": $Micheline}
```

PyTezos can generate empty storage based on the type description. This is a small part of the high-level interface
functionality we will further learn.

```python
>>> pytezos.origination(script=contract.script()).autofill().sign().inject()
'op3ZRdR6LjmA8AeNEjKEimr2uQeAWwXSXEftUBiTVx4k86Rw66m'

>>> opg = pytezos.shell.blocks[-5:].find_operation('op3ZRdR6LjmA8AeNEjKEimr2uQeAWwXSXEftUBiTVx4k86Rw66m')
>>> contract_id = opg['contents'][0]['metadata']['operation_result']['originated_contracts'][0]
>>> contract_id
'KT1RX74ty3TqBfU6pBs7ce3uV7PLBrUEav6X'
```

## Interact with contract



