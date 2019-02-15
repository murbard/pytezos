import requests
from functools import lru_cache

public_nodes = {
    'mainnet': ['https://rpc.tezrpc.me/', 'https://mainnet-node.tzscan.io/'],
    'zeronet': ['https://zeronet-node.tzscan.io/'],
    'alphanet': ['https://alphanet-node.tzscan.io/']
}


def urljoin(*args):
    return "/".join(map(lambda x: str(x).strip('/'), args))


class RpcError(ValueError):

    def __init__(self, res: requests.Response):
        super(RpcError, self).__init__(res.text)
        self.res = res

    def __str__(self):
        return f'{self.res.request.method} {self.res.request.url} <{self.res.status_code}>\n{self.res.text}'


class Node:

    def __init__(self, uri=public_nodes['mainnet'][0]):
        self._uri = uri
        self._cache = dict()

    def __repr__(self):
        return f'{self._uri}'

    def _request(self, method, path, **kwargs):
        res = requests.request(
            method=method,
            url=urljoin(self._uri, path),
            headers={'content-type': 'application/json'},
            **kwargs
        )
        if res.status_code != 200:
            raise RpcError(res)

        return res.json()

    def get(self, path, params=None, cache=False):
        if cache and path in self._cache:
            return self._cache[path]

        res = self._request('GET', path, params=params)
        if cache:
            self._cache[path] = res

        return res

    def post(self, path, json=None):
        return self._request('POST', path, json=json)


class RpcQuery:

    def __init__(self, path='', node=Node(), cache=False, sub_class=None):
        self._node = node
        self._path = path
        self._cache = cache

        if isinstance(sub_class, dict):
            self._sub_class = sub_class
        elif isinstance(sub_class, list):
            self._sub_class = {x: RpcQuery for x in sub_class}
        elif sub_class is not None:
            self._sub_class = {'_default': sub_class}
        else:
            self._sub_class = dict()

        if not self._sub_class.get('_default'):
            self._sub_class['_default'] = RpcQuery

    def __repr__(self):
        return self._path

    def __dir__(self):
        return sorted(list(super(RpcQuery, self).__dir__()) + list(self._sub_class.keys()))

    def __call__(self, *args, **kwargs):
        return self._node.get(
            path=self._path,
            params=kwargs,
            cache=self._cache
        )

    @lru_cache(maxsize=None)
    def __getattr__(self, item):
        if not item.startswith('_'):
            if item in self._sub_class:
                return self._sub_class[item](
                    path=f'{self._path}/{item}',
                    node=self._node,
                    cache=self._cache
                )
        raise AttributeError(item)

    @lru_cache(maxsize=None)
    def __getitem__(self, item):
        if isinstance(item, tuple):
            path = f'{self._path}/{item[0]}/{item[1]}'
        else:
            path = f'{self._path}/{item}'
        return self._sub_class['_default'](
            path=path,
            node=self._node,
            cache=self._cache
        )
