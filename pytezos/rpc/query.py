import re
from os.path import dirname

from pytezos.rpc.node import RpcNode
from pytezos.rpc.docs import rpc_docs


def get_attr_docstring(class_type, attr_name):
    if attr_name == 'get':
        attr_name = '__call__'

    attr = getattr(class_type, attr_name, None)
    if attr and attr.__doc__:
        return re.sub(r' {3,}', '', attr.__doc__)


def format_docstring(class_type, query_path):
    res = list()
    methods = {
        'GET': '()',
        'POST': '.post()',
        'PUT': '.put()',
        'DELETE': '.delete()'
    }
    rpc_doc = rpc_docs.get(query_path, {})

    for method, func in methods.items():
        if method in rpc_doc:
            docstring = get_attr_docstring(class_type, method.lower())
            if not docstring:
                docstring = f'\n{rpc_doc[method]["descr"]}\n'
                for arg in rpc_doc[method]['args']:
                    docstring += f':param {arg["name"]}: {arg["descr"]}\n'
                docstring += f':return: {rpc_doc[method]["ret"]}\n'

            res.append(f'{func}{docstring}')

    if 'item' in rpc_doc:
        docstring = get_attr_docstring(class_type, '__getitem__')
        if not docstring:
            item = rpc_doc["item"]
            docstring = f'\n:param {item["name"]}: {item["descr"]}\n:return: Child element\n'

        res.append(f'[]{docstring}')

    if 'props' in rpc_doc:
        properties = rpc_doc['props']
        docstring = '\n'.join(map(lambda x: f'.{x}', properties))
        res.append(f'RPC endpoints\n{docstring}\n')
    else:
        properties = list()

    helpers = filter(
        lambda x: not x.startswith('_') and x not in properties and x.upper() not in methods,
        dir(class_type))
    for helper in helpers:
        if type(getattr(class_type, helper)) == property:
            name = f'.{helper}'
        else:
            name = f'.{helper}()'
        docstring = get_attr_docstring(class_type, helper) or '\n'
        res.append(f'{name}{docstring}')

    return '\n'.join(res)


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

    def __init__(self, node: RpcNode, path='', caching=False, params=None, timeout=None):
        self._node = node
        self._path = path
        self._caching = caching
        self._timeout = timeout
        self._params = params or list()
        self.__doc__ = self._get_docstring()

    def _get_docstring(self):
        docstring = f'Path\n{self._query_path or "/"}\n\n'
        docstring += format_docstring(self.__class__, self._path)
        return docstring

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
                return self._spawn_query(
                    path=self._path + '/{}',
                    params=self._params + [attr]
                )
            else:
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
        return self.__doc__

    def _get(self, params=None):
        return self._node.get(
            path=self._query_path,
            params=params,
            caching=self._caching,
            timeout=self._timeout
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
        dir_path = dirname(self._path)
        return self._spawn_query(
            path=dir_path,
            params=self._params[:dir_path.count('{}')]
        )
