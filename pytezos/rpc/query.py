import re
import os

from pytezos.rpc.node import RpcNode, RpcError, urljoin

NO_INFO = 'No description ¯\\_(ツ)_/¯'


def get_attr_docstring(class_type, attr_name):
    if attr_name == 'get':
        attr_name = '__call__'

    attr = getattr(class_type, attr_name, None)
    if attr and attr.__doc__:
        return re.sub(r' {3,}', '', attr.__doc__)


def format_docstring(class_type, describe_tree):
    sections = list()

    for name, service in describe_tree['static'].items():
        if name.endswith('service'):
            method = {'GET': '()',
                      'POST': '.post()',
                      'PUT': '.put()',
                      'DELETE': '.delete()'}[service["meth"]]
            docstring = get_attr_docstring(class_type, service["meth"].lower())
            if not docstring:
                docstring = f'\n{service.get("description", NO_INFO)}\n'
                for arg in service.get('query', []):
                    docstring += f':param {arg["name"]}: {arg.get("description", NO_INFO)}\n'
                if service.get('output'):
                    return_type = service['output']['json_schema'].get('type', 'object').capitalize()
                    docstring += f':return: {return_type}\n'

            sections.append(f'{method}{docstring}')

    if describe_tree['static'].get('subdirs'):
        dynamic_dispatch = describe_tree['static']['subdirs'].get('dynamic_dispatch')
        if dynamic_dispatch:
            docstring = get_attr_docstring(class_type, '__getitem__')
            if not docstring:
                arg = dynamic_dispatch["arg"]
                docstring = f'\n:param {arg["name"]}: {arg.get("descr", NO_INFO)}\n:return: Child element\n'

            sections.append(f'[]{docstring}')

        suffixes = describe_tree['static']['subdirs'].get('suffixes')
        if suffixes:
            properties = list(map(lambda x: x['name'], suffixes))
            docstring = '\n'.join(map(lambda x: f'.{x}', properties))
            sections.append(f'RPC endpoints\n{docstring}\n')
        else:
            properties = list()

        helpers = filter(
            lambda x: not x.startswith('_') and x not in properties,
            dir(class_type))
        for helper in helpers:
            if type(getattr(class_type, helper)) == property:
                name = f'.{helper}'
            else:
                name = f'.{helper}()'
            docstring = get_attr_docstring(class_type, helper) or '\n'
            sections.append(f'{name}{docstring}')

    return '\n'.join(sections)


class RpcQuery:
    __extensions__ = dict()

    @classmethod
    def __init_subclass__(cls, path='', **kwargs):
        super().__init_subclass__(**kwargs)
        if isinstance(path, list):
            for sub_path in path:
                cls.__extensions__[sub_path] = cls
        else:
            cls.__extensions__[path] = cls

    def __init__(self, node: RpcNode, path='', caching=False, params=None):
        self._node = node
        self._path = path
        self._caching = caching
        self._params = params or list()

    def _spawn_query(self, path, params):
        child_class = self.__extensions__.get(path, RpcQuery)
        return child_class(
            path=path,
            node=self._node,
            caching=self._caching,
            params=params
        )

    @property
    def _query_path(self):
        return self._path.format(*self._params)

    def __call__(self, **params):
        return self._node.get(
            path=self._query_path,
            params=params,
            caching=self._caching
        )

    def __getattr__(self, attr):
        if not attr.startswith('_'):
            if attr in {'main', 'test', 'head', 'genesis'}:
                return self[attr]
            return self._spawn_query(
                path=f'{self._path}/{attr}',
                params=self._params
            )
        raise AttributeError(attr)

    def __getitem__(self, child_id):
        return self._spawn_query(
            path=self._path + '/{}',
            params=self._params + [child_id]
        )

    def __repr__(self):
        docstring = f'Path\n{self._query_path or "/"}\n\n'
        try:
            res = self._node.get(
                path=urljoin('describe', self._query_path),
                params=dict(recurse=True),
                caching=True,
                cache_key=f'/describe{self._path}'
            )
        except RpcError:
            return f'{docstring}\n\n{NO_INFO}'

        docstring += format_docstring(self.__class__, res)
        return docstring

    def _get(self, params=None):
        return self._node.get(
            path=self._query_path,
            params=params,
            caching=self._caching
        )

    def _post(self, json=None, params=None):
        return self._node.post(
            path=self._query_path,
            params=params,
            json=json,
            caching=self._caching
        )

    def _put(self, params=None):
        return self._node.put(
            path=self._query_path,
            params=params
        )

    def _delete(self, params=None):
        return self._node.delete(
            path=self._query_path,
            params=params
        )

    @property
    def _parent(self):
        dir_path = os.path.dirname(self._path)
        return self._spawn_query(
            path=dir_path,
            params=self._params[:dir_path.count('{}')]
        )
