import requests
import os

TEZRPC_MAINNET = 'https://rpc.tezrpc.me/'
TZSCAN_MAINNET = 'https://mainnet-node.tzscan.io/'
TZSCAN_ZERONET = 'https://zeronet-node.tzscan.io/'


class RpcError(ValueError):

    def __init__(self, res: requests.Response):
        super(RpcError, self).__init__(res.text)
        self.res = res

    def __str__(self):
        return f'{self.res.request.method} {self.res.request.url} <{self.res.status_code}>\n{self.res.text}'


class Node:

    def __init__(self, uri=TEZRPC_MAINNET):
        self.uri = uri

    def __repr__(self):
        return f'{self.uri}'

    def get(self, path, params=None):
        res = requests.get(
            url=os.path.join(self.uri, path),
            params=params,
            headers={'content-type': 'application/json'}
        )
        if res.status_code != 200:
            raise RpcError(res)

        return res.json()
