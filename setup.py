from setuptools import setup

setup(
    name='pytezos',
    version='0.1',
    description='Python utils for Tezos',
    url='https://github.com/baking-bad/pytezos',
    author='Arthur Breitman, Baking Bad',
    author_email='257byte@gmail.com',
    license='MIT',
    packages=['.'],
    zip_safe=False,
    install_requires=[
        'pysodium',
        'pyblake2',
        'base58',
        'secp256k1',
        'parameterized'
    ]
)
