import requests
from functools import lru_cache
from hashlib import sha1

public_nodes = {
    'mainnet': ['http://localhost:8732/', 'https://rpc.tezrpc.me/', 'https://mainnet-node.tzscan.io/'],
    'zeronet': ['http://localhost:8732/', 'https://zeronet-node.tzscan.io/'],
    'alphanet': ['http://localhost:8732/', 'https://alphanet-node.tzscan.io/']
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
        self._session = requests.Session()

    def __repr__(self):
        return f'{self._uri}'

    def _request(self, method, path, **kwargs):
        res = self._session.request(
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

    def post(self, path, json=None, cache=False):
        key = None
        if cache:
            key = sha1((path + str(json)).encode()).hexdigest()
            if key in self._cache:
                return self._cache[key]

        res = self._request('POST', path, json=json)
        if cache:
            self._cache[key] = res

        return res


class RpcQuery:

    def __init__(self, path='', node=Node(), cache=False, child_class=None, properties=None, **kwargs):
        self._node = node
        self._path = path
        self._cache = cache
        self._child_class = child_class if child_class else RpcQuery
        self._kwargs = kwargs

        if isinstance(properties, dict):
            self._properties = properties
        elif isinstance(properties, list):
            self._properties = {x: self._child_class for x in properties}
        else:
            self._properties = dict()

    def __repr__(self):
        return self._path

    def __dir__(self):
        return sorted(list(super(RpcQuery, self).__dir__())
                      + list(self._properties.keys()))

    def __call__(self, *args, **kwargs):
        return self._node.get(
            path=self._path,
            params=kwargs,
            cache=self._cache
        )

    @lru_cache(maxsize=None)
    def __getattr__(self, item):
        if not item.startswith('_'):
            child_class = self._properties.get(item, RpcQuery)
            return child_class(
                path=f'{self._path}/{item}',
                node=self._node,
                cache=self._cache,
                **self._kwargs
            )
        raise AttributeError(item)

    @lru_cache(maxsize=None)
    def __getitem__(self, item):
        return self._child_class(
            path=f'{self._path}/{item}',
            node=self._node,
            cache=self._cache,
            **self._kwargs
        )

    def get(self, key, default=None):
        data = self()
        if key in data:
            return data[key]
        if default is not None:
            return default
        raise KeyError(f'{key} is missing.')
