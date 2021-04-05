import sys
from glob import glob
from os.path import abspath, dirname, exists, join
from pprint import pformat
from typing import Optional

import click
import docker

from pytezos import ContractInterface, __version__, pytezos
from pytezos.cli.github import create_deployment, create_deployment_status
from pytezos.context.mixin import default_network  # type: ignore
from pytezos.logging import logger
from pytezos.michelson.types.base import generate_pydoc
from pytezos.operation.result import OperationResult
from pytezos.rpc.errors import RpcError

kernel_js_path = join(dirname(dirname(__file__)), 'assets', 'kernel.js')
kernel_json = {
    "argv": ['pytezos', 'kernel', 'run', "-file", "{connection_file}"],
    "display_name": "Michelson",
    "language": "michelson",
    "codemirror_mode": "michelson",
}


def make_bcd_link(network, address):
    return f'https://better-call.dev/{network}/{address}'


def get_local_contract_path(path, extension='tz'):
    if path is None:
        files = glob(f'*.{extension}')
        if len(files) != 1:
            raise Exception('No contracts found in working directory, specify --path implicitly')
        path = abspath(files[0])
    if exists(path):
        return path
    return False

def get_contract(path):
    path = get_local_contract_path(path)
    if path:
        contract = ContractInterface.from_file(path)
    else:
        network, address = path.split(':')
        contract = pytezos.using(shell=network).contract(address)
    return contract


def get_docker_client():
    return docker.from_env()


@click.group()
@click.version_option(__version__)
@click.pass_context
def cli(*_args, **_kwargs):
    pass


@cli.command(help='Manage contract storage')
@click.option('--action', '-a', type=str, help='One of `schema`, `default`.')
@click.option('--path', '-p', type=str, default=None, help='Path to the .tz file, or the following uri: <network>:<KT-address>')
@click.pass_context
def storage(_ctx, action: str, path: Optional[str]) -> None:
    contract = get_contract(path)
    if action == 'schema':
        logger.info(generate_pydoc(type(contract.storage.data), title='storage'))
    elif action == 'default':
        logger.info(pformat(contract.storage.dummy()))
    else:
        raise Exception('Action must be either `schema` or `default`')


@cli.command(help='Manage contract storage')
@click.option('--action', '-a', type=str, default='schema', help='One of `schema`')
@click.option('--path', '-p', type=str, default=None, help='Path to the .tz file, or the following uri: <network>:<KT-address>')
@click.pass_context
def parameter(_ctx, action: str, path: Optional[str]) -> None:
    contract = get_contract(path)
    if action == 'schema':
        logger.info(contract.parameter.__doc__)
    else:
        raise Exception('Action must be `schema`')


@cli.command(help='Activate and reveal key from the faucet file')
@click.option('--path', '-p', type=str, help='Path to the .json file downloaded from https://faucet.tzalpha.net/')
@click.option('--network', '-n', type=str, default=default_network, help='Default is edo2net')
@click.pass_context
def activate(_ctx, path: str, network: str) -> None:
    ptz = pytezos.using(key=path, shell=network)
    logger.info(
        'Activating %s in the %s',
        ptz.key.public_key_hash(),
        network,
    )

    if ptz.balance() == 0:
        try:
            opg = ptz.reveal().autofill().sign()
            logger.info('Injecting reveal operation:')
            logger.info(pformat(opg.json_payload()))
            opg.inject(_async=False)
        except RpcError as e:
            logger.critical(pformat(e))
            sys.exit(-1)
        else:
            logger.info('Activation succeeded! Claimed balance: %s ꜩ', ptz.balance())
    else:
        logger.info('Already activated')

    try:
        opg = ptz.reveal().autofill().sign()
        logger.info('Injecting reveal operation:')
        logger.info(pformat(opg.json_payload()))
        opg.inject(_async=False)
    except RpcError as e:
        logger.critical(pformat(e))
        sys.exit(-1)
    else:
        logger.info('Your key %s is now active and revealed', ptz.key.public_key_hash())


@cli.command(help='Deploy contract to the specified network')
@click.option('--path', '-p', type=str, help='Path to the .tz file')
@click.option('--storage', type=str, default=None, help='Storage in JSON format (not Micheline)')
@click.option('--network', '-n', type=str, default=default_network, help='Default is edo2net')
@click.option('--key', type=str, default=None)
@click.option('--github-repo-slug', type=str, default=None)
@click.option('--github-oauth-token', type=str, default=None)
@click.option('--dry-run', type=bool, default=False, help='Set this flag if you just want to see what would happen')
@click.pass_context
def deploy(
    _ctx,
    path: str,
    storage: Optional[str],  # pylint: disable=redefined-outer-name
    network: str,
    key: Optional[str],
    github_repo_slug: Optional[str],
    github_oauth_token: Optional[str],
    dry_run: bool,
):
    ptz = pytezos.using(shell=network, key=key)
    logger.info('Deploying contract using %s in the %s', ptz.key.public_key_hash(), network)

    contract = get_contract(path)
    try:
        opg = ptz.origination(script=contract.script(initial_storage=storage)).autofill().sign()
        logger.info('Injecting origination operation:')
        logger.info(pformat(opg.json_payload()))

        if dry_run:
            logger.info(pformat(opg.preapply()))
            sys.exit(0)
        else:
            opg = opg.inject(_async=False)
    except RpcError as e:
        logger.critical(pformat(e))
        sys.exit(-1)
    else:
        originated_contracts = OperationResult.originated_contracts(opg)
        if len(originated_contracts) != 1:
            raise Exception('Operation group must has exactly one originated contract')
        bcd_link = make_bcd_link(network, originated_contracts[0])
        logger.info('Contract was successfully deployed: %s', bcd_link)

        if github_repo_slug:
            deployment = create_deployment(
                github_repo_slug,
                github_oauth_token,
                environment=network,
            )
            logger.info(pformat(deployment))
            status = create_deployment_status(
                github_repo_slug,
                github_oauth_token,
                deployment_id=deployment['id'],
                state='success',
                environment=network,
                environment_url=bcd_link,
            )
            logger.info(status)


@cli.command(help='Update Ligo compiler (docker pull ligolang/ligo)')
@click.option('--tag', '-t', type=str, help='Version or tag to pull', default='0.13.0')
@click.pass_context
def update_ligo(
    _ctx,
    tag: str,
):
    client = get_docker_client()
    logger.info(f'Pulling ligolang/ligo{(":" + tag) if tag else ""}, please stay put.')
    client.images.pull('ligolang/ligo', tag=tag)
    logger.info('Pulled Ligo compiler image successfully!')


def run_ligo_container(
    tag: str = '0.13.0',
    command: str = '',
):
    try:
        client = get_docker_client()
        return client.containers.run(image=f'ligolang/ligo:{tag}', command=comand)
    except docker.errors.ImageNotFound:
        logger.error('Ligo compiler not found. Please run update-ligo first.')


@cli.command(help='Compile contract using Ligo compiler.')
@click.option('--tag', '-t', type=str, help='Version or tag of Ligo compiler', default='0.13.0')
@click.option('--path', '-p', type=str, help='Path to contract', default='0.13.0')
@click.pass_context
def ligo_compile_contract(
    _ctx,
    tag: str,
    path: str,
):
    path = get_local_contract_path(path, extension='ligo')
    if path:
        run_ligo_container(tag=tag, command=f'compile-contract {path}')
    else:
        logger.error('No local contract found. Please ensure a valid contract is present or specify path.')


@cli.command(help='Define initial storage using Ligo compiler.')
@click.option('--tag', '-t', type=str, help='Version or tag of Ligo compiler', default='0.13.0')
@click.option('--path', '-p', type=str, help='Path to contract')
@click.option('--entry-point', '-ep', type=str, help='Entrypoint for the storage')
@click.option('--expression', '-ex', type=str, help='Expression for the storage')
@click.pass_context
def ligo_compile_contract(
    _ctx,
    tag: str,
    path: str,
    entry_point: str,
    expression: str,
):
    path = get_local_contract_path(path)
    if path:
        run_ligo_container(tag=tag, command=f'compile-storage {path} {entry_point} {expression}')
    else:
        logger.error('No local contract found. Please ensure a valid contract is present or specify path.')


@cli.command(help='Invoke a contract with a parameter using Ligo compiler.')
@click.option('--tag', '-t', type=str, help='Version or tag of Ligo compiler', default='0.13.0')
@click.option('--path', '-p', type=str, help='Path to contract')
@click.option('--entry-point', '-ep', type=str, help='Entrypoint for the invocation')
@click.option('--expression', '-ex', type=str, help='Expression for the invocation')
@click.pass_context
def ligo_invoke_contract(
    _ctx,
    tag: str,
    path: str,
    entry_point: str,
    expression: str,
):
    path = get_local_contract_path(path)
    if path:
        run_ligo_container(tag=tag, command=f'compile-parameter {path} {entry_point} {expression}')
    else:
        logger.error('No local contract found. Please ensure a valid contract is present or specify path.')


if __name__ == '__main__':
    cli(prog_name='pytezos')
