from pytezos import Key


if __name__ == '__main__':
    print(Key.from_encoded_key('edsk3nM41ygNfSxVU4w1uAW3G9EnTQEB5rjojeZedLTGmiGRcierVv'))
    print(Key.from_encoded_key('edpku976gpuAD2bXyx1XGraeKuCo1gUZ3LAJcHM12W1ecxZwoiu22R'))
    print(Key.from_secret_exponent(b'\x92T-\x86jRc\x11Z\xa4\x16\xfd>\x1d\xceL\xed5\xf5TT\x17\xd1\xf77c\xf7\t5R\xa7+A'
                                   b'\x94\x91\xb1yk\x13\xd7V\xd3\x94\xed\x92\\\x10r{\xca\x06\xe9sS\xc5\xca\t@*\x9bk'
                                   b'\x07\xab\xcc'))
    print(Key.from_public_point(b'A\x94\x91\xb1yk\x13\xd7V\xd3\x94\xed\x92\\\x10r{\xca\x06\xe9sS\xc5\xca\t@*\x9bk\x07'
                                b'\xab\xcc'))
    print(Key.from_mnemonic('ensure vague decline floor negative dilemma actual better hidden flat vapor ride fiction '
                            'fuel laundry harsh strong retire lunch vivid find outer gloom current',
                            passphrase='qwerty', email='user@example.com'))
    print(Key.from_encoded_key(
        key='spesk21cruoqtYmxfq5fpkXiZZRLRw4vh7VFJauGCAgHxZf3q6Q5LTv9m9dnMxyVjna6RzWQL45q4ppGLh97xZpV',
        passphrase='qqq'
    ))
