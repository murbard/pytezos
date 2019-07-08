import requests
from hashlib import sha1
from urllib.parse import urlencode
import logging


def urljoin(*args):
    return "/".join(map(lambda x: str(x).strip('/'), args))


class RpcError(ValueError):

    def __init__(self, res: requests.Response):
        super(RpcError, self).__init__(res.text)
        self.res = res

    def __str__(self):
        return f'{self.res.request.method} {self.res.request.url} <{self.res.status_code}>\n{self.res.text}'


class RpcNode:

    def __init__(self, uri):
        self._uri = uri
        self._cache = dict()
        self._session = requests.Session()

    def __repr__(self):
        return f'Node address\n{self._uri}\n\nCached items\n' + '\n'.join(self._cache.keys())

    def request(self, method, path, **kwargs) -> requests.Response:
        res = self._session.request(
            method=method,
            url=urljoin(self._uri, path),
            headers={'content-type': 'application/json'},
            **kwargs
        )
        if res.status_code != 200:
            raise RpcError(res)

        return res

    def get(self, path, params=None, caching=False, cache_key=None):
        if caching:
            if not cache_key:
                cache_key = path + f'?{urlencode(params)}' if params else ''
            if cache_key in self._cache:
                return self._cache[cache_key]

        res = self.request('GET', path, params=params).json()
        if caching:
            self._cache[cache_key] = res

        return res

    def post(self, path, params=None, json=None, caching=False):
        cache_key = None
        if caching:
            cache_key = sha1((path + str(json)).encode()).hexdigest()
            if cache_key in self._cache:
                return self._cache[cache_key]

        res = self.request('POST', path, params=params, json=json).json()
        if caching:
            self._cache[cache_key] = res

        return res

    def delete(self, path, params=None):
        return self.request('DELETE', path, params=params).json()

    def put(self, path, params=None):
        return self.request('PUT', path, params=params).json()


