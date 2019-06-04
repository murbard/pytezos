import requests
import re
from hashlib import sha1

METHODS = {
    'GET': '()',
    'POST': '.post()',
    'PUT': '.put()',
    'DELETE': '.delete()'
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

    def __init__(self, uri):
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

    def post(self, path, params=None, json=None, cache=False):
        key = None
        if cache:
            key = sha1((path + str(json)).encode()).hexdigest()
            if key in self._cache:
                return self._cache[key]

        res = self._request('POST', path, params=params, json=json)
        if cache:
            self._cache[key] = res

        return res

    def delete(self, path, params=None):
        return self._request('DELETE', path, params=params)

    def put(self, path, params=None):
        return self._request('PUT', path, params=params)


class RpcQuery:

    def __init__(self, node, path="", cache=False, child_class=None, properties=None, **kwargs):
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

    def __dir__(self):
        return sorted(list(super(RpcQuery, self).__dir__())
                      + list(self._properties.keys()))

    def __call__(self, **params):
        return self._node.get(
            path=self._path,
            params=params,
            cache=self._cache
        )

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

    def __getitem__(self, item):
        return self._child_class(
            path=f'{self._path}/{item}',
            node=self._node,
            cache=self._cache,
            **self._kwargs
        )

    def _get_docstring(self, name):
        if name == 'get':
            name = '__call__'

        function = getattr(self, name, None)
        if function and function.__doc__:
            return re.sub(r' {3,}', '', function.__doc__)

    def __repr__(self):
        try:
            res = self._node.get(
                path=urljoin('describe', self._path),
                params=dict(recurse=True),
                cache=True
            )
        except RpcError:
            return 'No documentation available for this endpoint'

        sections = [f'Path\n{self._path}\n']

        for name, service in res['static'].items():
            if not name.endswith('service'):
                continue

            method = f'{METHODS[service["meth"]]}'
            docstring = self._get_docstring(service["meth"].lower())
            if not docstring:
                docstring = f'\n{service.get("description", "Self-explanatory")}\n'
                for arg in service.get('query', []):
                    docstring += f':param {arg["name"]}: {arg.get("description", "Self-explanatory")}\n'
                if service.get('output'):
                    return_type = service['output']['json_schema'].get('type', 'object').capitalize()
                    docstring += f':return: {return_type}\n'

            method += docstring
            sections.append(method)

        if res['static'].get('subdirs'):
            dynamic_dispatch = res['static']['subdirs'].get('dynamic_dispatch')
            if dynamic_dispatch:
                get_item = f'[]'
                docstring = self._get_docstring('__getitem__')
                if not docstring:
                    arg = dynamic_dispatch["arg"]
                    docstring = f'\n:param {arg["name"]}: {arg["descr"]}\n:return: Child element'

                get_item += docstring
                sections.append(get_item)

            suffixes = res['static']['subdirs'].get('suffixes')
            if suffixes:
                sections.append('Properties\n{}'.format(
                    '\n'.join(map(lambda x: f'.{x["name"]}', suffixes))))

        return '\n'.join(sections)
