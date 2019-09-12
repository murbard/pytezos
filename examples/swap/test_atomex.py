from os.path import dirname, join
from unittest import TestCase
from decimal import Decimal

from pytezos import ContractInterface, pytezos, format_timestamp, MichelsonRuntimeError

"""
$parameter:
    { "initiate": $initiate } || 
    { "add": $bytes  /* hashed_secret */ } || 
    { "redeem": $bytes  /* secret */ } || 
    { "refund": $bytes  /* hashed_secret */ }

$initiate:
    {
      "participant": $address,
      "settings": $settings
    }

$settings:
    {
      "hashed_secret": $bytes,
      "refund_time": $timestamp,
      "payoff": $mutez
    }
"""

"""
$storage:
    [ { $bytes : $0_item , ... }  /* big_map */ , $unit ]

$0_item:
    {
      "recipients": $recipients,
      "settings": $settings
    }

$settings:
    {
      "amount": $mutez,
      "refund_time": $timestamp,
      "payoff": $mutez
    }

$recipients:
    {
      "initiator": $address,
      "participant": $address
    }
"""

source = 'tz1irF8HUsQp2dLhKNMhteG1qALNU9g3pfdN'
party = 'tz1h3rQ8wBxFd8L9B3d7Jhaawu6Z568XU3xY'
hashed_secret = '05bce5c12071fbca95b13d49cb5ef45323e0216d618bb4575c519b74be75e3da'
empty_storage = [{}, None]


class AtomexContractTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.atomex = ContractInterface.create_from(join(dirname(__file__), 'atomex.tz'))
        cls.maxDiff = None

    def test_initiate(self):
        now = pytezos.now()

        res = self.atomex \
            .initiate(participant=party,
                      settings=dict(
                          hashed_secret=hashed_secret,
                          refund_time=now + 6 * 3600,
                          payoff=Decimal('0.02')
                      )) \
            .with_amount(Decimal('1')) \
            .result(storage=empty_storage,
                    source=source)

        big_map_diff = {
            hashed_secret: {
                'recipients': {
                    'initiator': source,
                    'participant': party
                },
                'settings': {
                    'amount': Decimal('0.98'),
                    'refund_time': format_timestamp(now + 6 * 3600),
                    'payoff': Decimal('0.02')
                }
            }
        }
        self.assertDictEqual(big_map_diff, res.big_map_diff)
        self.assertEqual(empty_storage, res.storage)
        self.assertEqual([], res.operations)

    def test_initiate_same_secret(self):
        now = pytezos.now()
        initial_storage = [{
            hashed_secret: {
                'recipients': {
                    'initiator': source,
                    'participant': party
                },
                'settings': {
                    'amount': Decimal('0.98'),
                    'refund_time': format_timestamp(now + 6 * 3600),
                    'payoff': Decimal('0.02')
                }
            }
        }, None]

        with self.assertRaises(MichelsonRuntimeError):
            self.atomex \
                .initiate(participant=party,
                          settings=dict(
                              hashed_secret=hashed_secret,
                              refund_time=now + 6 * 3600,
                              payoff=Decimal('0.02')
                          )) \
                .with_amount(Decimal('1')) \
                .result(storage=initial_storage,
                        source=source)

    def test_initiate_payoff_overflow(self):
        now = pytezos.now()

        with self.assertRaises(MichelsonRuntimeError):
            self.atomex \
                .initiate(participant=party,
                          settings=dict(
                              hashed_secret=hashed_secret,
                              refund_time=now - 3600,
                              payoff=Decimal('1.1')
                          )) \
                .with_amount(Decimal('1')) \
                .result(storage=empty_storage,
                        source=source)

    def test_add_non_existent(self):
        with self.assertRaises(MichelsonRuntimeError):
            self.atomex \
                .add(hashed_secret) \
                .with_amount(Decimal('1')) \
                .result(storage=empty_storage)

    def test_add(self):
        now = pytezos.now()
        initial_storage = [{
            hashed_secret: {
                'recipients': {
                    'initiator': source,
                    'participant': party
                },
                'settings': {
                    'amount': Decimal('0.98'),
                    'refund_time': format_timestamp(now + 6 * 3600),
                    'payoff': Decimal('0.02')
                }
            }
        }, None]

        res = self.atomex \
            .add(hashed_secret) \
            .with_amount(Decimal('1')) \
            .result(storage=initial_storage, source=source)

        big_map_diff = initial_storage[0]
        big_map_diff[hashed_secret]['settings']['amount'] = Decimal('1.98')
        self.assertDictEqual(big_map_diff, res.big_map_diff)
