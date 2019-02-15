import requests
import os

public_nodes = {
    'mainnet': ['https://rpc.tezrpc.me/', 'https://mainnet-node.tzscan.io/'],
    'zeronet': ['https://zeronet-node.tzscan.io/'],
    'alphanet': ['https://alphanet-node.tzscan.io/']
}


class RpcError(ValueError):

    def __init__(self, res: requests.Response):
        super(RpcError, self).__init__(res.text)
        self.res = res

    def __str__(self):
        return f'{self.res.request.method} {self.res.request.url} <{self.res.status_code}>\n{self.res.text}'


class Node:

    def __init__(self, uri=public_nodes['mainnet'][0]):
        self.uri = uri

    def __repr__(self):
        return f'{self.uri}'

    def _request(self, method, path, **kwargs):
        res = requests.request(
            method=method,
            url=os.path.join(self.uri, path),
            headers={'content-type': 'application/json'},
            **kwargs
        )
        if res.status_code != 200:
            raise RpcError(res)

        return res.json()

    def get(self, path, params=None):
        return self._request('GET', path, params=params)

    def post(self, path, json=None):
        return self._request('POST', path, json=json)
