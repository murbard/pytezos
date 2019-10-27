import requests
from os.path import join
from urllib.parse import urlparse


def get_base_dir(repo_url):
    return join('https://api.github.com/repos', urlparse(repo_url).path)


def create_deployment(repo_url, oauth_token, environment, ref='master'):
    return requests.post(
        url=join(get_base_dir(repo_url), 'deployments'),
        headers={
            'Accept': 'application/vnd.github.ant-man-preview+json',
            'Authorization': f'token {oauth_token}'
        },
        json={
            'ref': ref,
            'environment': environment
        }).json()


def create_deployment_status(repo_url, oauth_token, deployment_id, state, environment, environment_url=None):
    assert state in {'success', 'failure'}
    return requests.post(
        url=join(get_base_dir(repo_url), 'deployments', deployment_id, 'statuses'),
        headers={
            'Accept': 'application/vnd.github.flash-preview+json',
            'Authorization': f'token {oauth_token}'
        },
        json={
            'state': state,
            'environment': environment,
            'environment_url': environment_url
        }).json()
