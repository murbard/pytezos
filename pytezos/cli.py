import fire
from os.path import abspath
from glob import glob
from pprint import pprint

from pytezos import pytezos, Contract
from pytezos.michelson.docstring import generate_docstring


def get_contract(path):
    if path is None:
        files = glob('*.tz')
        assert len(files) == 1
        contract = Contract.from_file(abspath(files[0]))

    elif any(map(lambda x: path.startswith(x), ['zeronet', 'alphanet', 'mainnet'])):
        network, address = path.split(':')
        ptz = pytezos.using(shell=network)
        script = ptz.shell.contracts[address].script()
        contract = Contract.from_micheline(script['code'])

    else:
        contract = Contract.from_file(path)

    return contract


class PyTezosCli:

    def storage(self, action, path=None):
        """
        :param action: One of `schema`, `default`
        :param path: Path to the .tz file, or the following uri: <network>:<KT-address>
        """
        contract = get_contract(path)
        if action == 'schema':
            print(generate_docstring(contract.storage.schema, title='storage'))
        elif action == 'default':
            pprint(contract.storage.default())
        else:
            assert False, action

    def parameter(self, action, path=None):
        """
        :param action: One of `schema`
        :param path: Path to the .tz file, or the following uri: <network>:<KT-address>
        """
        contract = get_contract(path)
        if action == 'schema':
            print(generate_docstring(contract.parameter.schema, title='parameter'))
        else:
            assert False, action

    def activate(self, path, dry_run=False):
        """
        Activate faucet key
        :param path: Path to the .json file downloaded from https://faucet.tzalpha.net/
        :param dry_run: Set this flag if you just want to see what would happen
        """
        opg = pytezos.using(key=path).activate_account().autofill().sign()
        if dry_run:
            pprint(opg.preapply())
        else:
            opg.inject()
            print(f'Congrats! Soon your will be able to use your key.')

    def reveal(self, dry_run=False):
        """
        Reveal public key
        :param dry_run: Set this flag if you just want to see what would happen
        """
        pass

    def deploy(self, path=None, storage=None, dry_run=False):
        """
        Deploy contract to the alphane
        :param path: Path to the .tz file
        :param storage: Storage in JSON format (not Micheline)
        :param dry_run: Set this flag if you just want to see what would happen
        """
        contract = get_contract(path)
        if storage is not None:
            storage = contract.storage.encode(storage)

        script = contract.script(storage=storage)
        opg = pytezos.origination(script=script).autofill().sign()
        if dry_run:
            pprint(opg.preapply())
        else:
            opg_hash = opg.inject()
            print(f'As soon as your origination is included in a block, '
                  f'you can check it at https://better-call.dev/{opg_hash}')

    def test(self, action=None, path=None):
        """
        :param action: On of `init`
        :param path: Path to the .tz file
        """


def main():
    return fire.Fire(PyTezosCli)


if __name__ == '__main__':
    main()
