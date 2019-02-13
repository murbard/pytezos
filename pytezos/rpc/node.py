import requests
import os

predefined = {
    'mainnet': ['https://rpc.tezrpc.me/', 'https://mainnet-node.tzscan.io/'],
    'zeronet': ['https://zeronet-node.tzscan.io/']
}


class Node:

    def __init__(self, uri=predefined['mainnet'][0]):
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
            raise requests.HTTPError(dict(
                code=res.status_code,
                message=res.text,
                requested_url=res.url
            ))

        return res.json()
