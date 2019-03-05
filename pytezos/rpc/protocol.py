import os
import tarfile
import requests
from difflib import unified_diff
from functools import lru_cache
from binascii import hexlify
from collections import defaultdict
from glob import glob
from tempfile import mkstemp, mkdtemp

from pytezos.rpc.node import RpcQuery


@lru_cache(maxsize=None)
def load_protocol(uri) -> dict:
    """
    Loads protocol implementation from various sources and converts it to the RPC-like format
    :param uri: link/path to a tar archive or path to a folder with extracted contents
    :return: dictionary, containing a list of hexified .ml/.mli files
    """
    try:
        res = requests.get(uri, stream=True)
        file, uri = mkstemp()
        try:
            for data in res.iter_content():
                file.write(data)
        finally:
            file.close()
    except ValueError:
        pass

    if os.path.isfile(uri):
        tar = tarfile.open(uri)
        try:
            uri = mkdtemp()
            tar.extractall(uri)
        finally:
            tar.close()

    if not os.path.isdir(uri):
        raise ValueError('Not a directory.')

    components = defaultdict(dict)
    for filename in glob(os.path.join(uri, '*.ml*')):
        name, ext = os.path.basename(filename).split('.')
        with open(filename, 'r') as file:
            source = file.read()

        key = {'mli': 'interface', 'ml': 'implementation'}[ext]
        components[name.capitalize()][key] = hexlify(source.encode()).decode()

    proto = dict(components=[
        dict(name=name, **component)
        for name, component in components.items()
    ])
    return proto


class Protocol(RpcQuery):

    def __init__(self, uri=None, *args, **kwargs):
        if kwargs.get('path'):
            path = kwargs['path']
        elif uri:
            path = uri.rstrip('/')
        else:
            raise NotImplementedError
        kwargs['protocol_id'] = os.path.basename(path)
        super(Protocol, self).__init__(*args, **kwargs)
        self._uri = uri if uri else None

    def __repr__(self):
        if self._uri:
            return self._uri
        return super(Protocol, self).__repr__()

    def __call__(self, *args, **kwargs):
        if self._uri:
            return load_protocol(self._uri)
        return super(Protocol, self).__call__(*args, **kwargs)

    def __iter__(self):
        data = self()
        extensions = {'interface': 'mli', 'implementation': 'ml'}
        for component in data.get('components', []):
            for key, ext in extensions.items():
                if key in component:
                    filename = f'{component["name"].lower()}.{ext}'
                    source = bytes.fromhex(component[key]).decode()
                    yield filename, source

    def diff(self, proto) -> list:
        """
        Calculates file diff between two protocol versions
        :param proto: an instance of Protocol
        :return: list of patches (file by file)
        """
        assert isinstance(proto, Protocol)

        def get_lines(p):
            return dict(map(lambda x: (x[0], x[1].split('\n')), iter(p)))

        a = get_lines(self)
        b = get_lines(proto)
        filenames = set(a.keys()).union(set(b.keys()))

        diff_lines = [
            unified_diff(
                a=a.get(filename, []),
                b=b.get(filename, []),
                fromfile=filename,
                tofile=filename,
                fromfiledate=self._kwargs['protocol_id'],
                tofiledate=proto._kwargs['protocol_id']
            )
            for filename in filenames
        ]
        return list(map(lambda x: '\n'.join(x), diff_lines))
