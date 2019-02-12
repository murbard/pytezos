import requests
import os

predefined = {
    'main': ['https://rpc.tezrpc.me/']
}


class Node:

    def __init__(self, chain_id='main', uri=predefined['main'][0]):
        self.chain_id = chain_id
        self.uri = uri

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
