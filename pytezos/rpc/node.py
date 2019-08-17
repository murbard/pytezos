import requests
from json import JSONDecodeError
from hashlib import sha1
from urllib.parse import urlencode


def urljoin(*args):
    return "/".join(map(lambda x: str(x).strip('/'), args))


class RpcError(ValueError):

    def __init__(self, res: requests.Response):
        super(RpcError, self).__init__(res.text)
        self.res = res

    def __str__(self):
        return f'{self.res.request.method} {self.res.request.url} <{self.res.status_code}>\n{self.res.text}'


class RpcNode:

    def __init__(self, uri, network=''):
        self.uri = uri
        self.network = network
        self._cache = dict()
        self._session = requests.Session()

    def __repr__(self):
        res = [
            super(RpcNode, self).__repr__(),
            '\nNode address',
            f'{self.uri} ({self.network})',
            '\nCached urls',
            *list(self._cache.keys())
        ]
        return '\n'.join(res)

    def request(self, method, path, **kwargs) -> requests.Response:
        res = self._session.request(
            method=method,
            url=urljoin(self.uri, path),
            headers={
                'content-type': 'application/json',
                'user-agent': 'PyTezos'
            },
            **kwargs
        )
        if res.status_code != 200:
            raise RpcError(res)

        return res

    def get(self, path, params=None, caching=False, cache_key=None, timeout=None):
        if caching:
            if not cache_key:
                cache_key = path
                if params:
                    cache_key += f'?{urlencode(params)}'
            if cache_key in self._cache:
                return self._cache[cache_key]

        res = self.request('GET', path, params=params, timeout=timeout).json()
        if caching:
            self._cache[cache_key] = res

        return res

    def post(self, path, params=None, json=None, caching=False):
        cache_key = None
        if caching:
            cache_key = sha1((path + str(json)).encode()).hexdigest()
            if cache_key in self._cache:
                return self._cache[cache_key]

        response = self.request('POST', path, params=params, json=json)
        try:
            res = response.json()
        except JSONDecodeError:
            res = response.text

        if caching:
            self._cache[cache_key] = res

        return res

    def delete(self, path, params=None):
        return self.request('DELETE', path, params=params).json()

    def put(self, path, params=None):
        return self.request('PUT', path, params=params).json()
