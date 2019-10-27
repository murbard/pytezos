import fire
from os.path import abspath
from glob import glob
from pprint import pprint

from pytezos import pytezos, Contract
from pytezos.operation.result import OperationResult
from pytezos.michelson.docstring import generate_docstring
from pytezos.tools.github import create_deployment, create_deployment_status


def make_bcd_link(network, address):
    net = {
        'babylonnet': 'babylon',
        'sandboxnet': 'sandbox',
        'mainnet': 'mainnet',
        'zeronet': 'zeronet'
    }
    return f'https://better-call.dev/{net[network]}/{address}'


def get_contract(path):
    if path is None:
        files = glob('*.tz')
        assert len(files) == 1
        contract = Contract.from_file(abspath(files[0]))

    elif any(map(lambda x: path.startswith(x), ['zeronet', 'babylonnet', 'mainnet'])):
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

    def activate(self, path, network='babylonnet'):
        """
        Activates and reveals faucet key
        :param path: Path to the .json file downloaded from https://faucet.tzalpha.net/
        :param dry_run: Set this flag if you just want to see what would happen
        """
        print('Initializing network and key')
        ptz = pytezos.using(key=path, shell=network)

        print(f'Sending activate account operation')
        opg = ptz.activate_account().autofill().sign().inject(_async=False)
        if not OperationResult.is_applied(opg):
            raise ValueError(OperationResult.errors(opg))

        print(f'Sending reveal operation')
        opg = ptz.reveal().autofill().sign().inject(_async=False)
        if not OperationResult.is_applied(opg):
            raise ValueError(OperationResult.errors(opg))

        print(f'Your key {ptz.key.public_key_hash()} is now active and revealed')

    def deploy(self, path=None, storage=None, network='babylonnet', key=None,
               github_repo=None, github_oauth_token=None, dry_run=False):
        """
        Deploy contract to the specified network
        :param path: Path to the .tz file
        :param storage: Storage in JSON format (not Micheline)
        :param network:
        :param key:
        :param github_repo:
        :param github_oauth_token:
        :param dry_run: Set this flag if you just want to see what would happen
        """
        print('Initializing network and key')
        ptz = pytezos.using(shell=network, key=key)

        print('Parsing contract and storage data')
        contract = get_contract(path)
        if storage is not None:
            storage = contract.storage.encode(storage)

        print('Preparing operation group')
        script = contract.script(storage=storage)
        opg = ptz.origination(script=script).autofill().sign()

        if dry_run:
            pprint(opg.preapply())
        else:
            print('Injecting operation group and waiting for inclusion')
            opg_with_metadata = opg.inject(_async=False)
            if not OperationResult.is_applied(opg_with_metadata):
                raise ValueError(OperationResult.errors(opg_with_metadata))
            else:
                print('Operation group is applied, parsing metadata')

            originated_contracts = OperationResult.originated_contracts(opg_with_metadata)
            assert len(originated_contracts) == 1
            bcd_link = make_bcd_link(network, originated_contracts[0])
            print(f'Contract was successfully deployed: {bcd_link}')

            # if github_repo:
            #     deployment = create_deployment(github_repo, github_oauth_token, environment=network)
            #     create_deployment_status(github_repo, github_oauth_token, deployment['id'],
            #                              state='success', environment=network, environment_url=bcd_link)


def main():
    return fire.Fire(PyTezosCli)


if __name__ == '__main__':
    main()
