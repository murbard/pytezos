import os
import tarfile
import requests
import io
import netstruct
import simplejson as json
from functools import lru_cache
from binascii import hexlify
from collections import OrderedDict
from typing import List, Tuple
from tempfile import mkstemp, mkdtemp
from diff_match_patch import diff_match_patch

from pytezos.rpc.node import RpcQuery
from pytezos.crypto import blake2b_32
from pytezos.encoding import base58_encode


def dir_to_files(path) -> List[Tuple[str, str]]:
    files = list()

    with open(os.path.join(path, 'TEZOS_PROTOCOL')) as f:
        index = json.load(f)

    for module in index['modules']:
        for ext in ['mli', 'ml']:
            name = f'{module.lower()}.{ext}'

            filename = os.path.join(path, name)
            if not os.path.exists(filename):
                continue

            with open(filename, 'r') as file:
                text = file.read()
                files.append((name, text))

    return files


def tar_to_files(path=None, raw=None) -> List[Tuple[str, str]]:
    assert path or raw

    fileobj = io.BytesIO(raw) if raw else None
    with tarfile.open(name=path, fileobj=fileobj) as tar:
        folder = mkdtemp()
        tar.extractall(folder)

    return dir_to_files(folder)


def url_to_files(url) -> List[Tuple[str, str]]:
    res = requests.get(url, stream=True)
    file, path = mkstemp()
    try:
        for data in res.iter_content():
            file.write(data)
    finally:
        file.close()

    return tar_to_files(path)


def files_to_proto(files: List[Tuple[str, str]]) -> dict:
    components = OrderedDict()

    for filename, text in files:
        name, ext = filename.split('.')
        key = {'mli': 'interface', 'ml': 'implementation'}[ext]
        name = name.capitalize()
        data = hexlify(text.encode()).decode()

        if name in components:
            components[name][key] = data
        else:
            components[name] = {'name': name, key: data}

    proto = {
        'expected_env_version': 0,
        'components': list(components.values())
    }
    return proto


def files_to_tar(files: List[Tuple[str, str]], path=None):
    fileobj = io.BytesIO() if path is None else None

    with tarfile.open(name=path, fileobj=fileobj, mode='w') as tar:
        for filename, text in files:
            file = io.BytesIO(text.encode())
            ti = tarfile.TarInfo(filename)
            ti.size = len(file.getvalue())
            tar.addfile(ti, file)

    if fileobj:
        return fileobj.getvalue()


def proto_to_files(proto: dict) -> List[Tuple[str, str]]:
    files = list()
    extensions = {'interface': 'mli', 'implementation': 'ml'}

    for component in proto.get('components', []):
        for key, ext in extensions.items():
            if key in component:
                filename = f'{component["name"].lower()}.{ext}'
                text = bytes.fromhex(component[key]).decode()
                files.append((filename, text))

    return files


def proto_to_bytes(proto: dict) -> bytes:
    res = b''

    for component in proto.get('components', []):
        res += netstruct.pack(b'I$', component['name'].encode())
        if component.get('interface'):
            res += b'\xff' + netstruct.pack(b'I$', bytes.fromhex(component['interface']))
        else:
            res += b'\x00'
        res += netstruct.pack(b'I$', bytes.fromhex(component['implementation']))

    res = netstruct.pack(b'hI$', proto['expected_env_version'], res)
    return res


class Protocol(RpcQuery):

    def __init__(self, data=None, *args, **kwargs):
        super(Protocol, self).__init__(*args, **kwargs)
        self._data = data

    def __repr__(self):
        if self._data:
            return str(self._data)
        return super(Protocol, self).__repr__()

    def __call__(self, *args, **kwargs):
        if self._data:
            return self._data
        return super(Protocol, self).__call__(*args, **kwargs)

    def __iter__(self):
        return iter(proto_to_files(self()))

    @classmethod
    @lru_cache(maxsize=None)
    def from_uri(cls, uri):
        """
        Loads protocol implementation from various sources and converts it to the RPC-like format
        :param uri: link/path to a tar archive or path to a folder with extracted contents
        :return: Protocol instance
        """
        if uri.startswith('http'):
            files = url_to_files(uri)
        elif os.path.isfile(uri):
            files = tar_to_files(uri)
        elif os.path.isdir(uri):
            files = dir_to_files(uri)
        else:
            raise ValueError(uri)

        return Protocol(data=files_to_proto(files))

    def index(self):
        proto = self()
        data = {
            'hash': self.calculate_hash(),
            'modules': list(map(lambda x: x['name'], proto.get('components', [])))
        }
        return data

    def export_tar(self, path=None):
        files = proto_to_files(self())
        files.append(('TEZOS_PROTOCOL', json.dumps(self.index())))
        return files_to_tar(files, path)

    def make_patch(self, proto, context_lines=3):
        """
        Calculates file diff between two protocol versions
        :param proto: an instance of Protocol
        :return: patch in proto format
        """
        assert isinstance(proto, Protocol)

        a = dict(iter(self))
        b = dict(iter(proto))
        filenames = set(a.keys()).union(set(b.keys()))

        dmp = diff_match_patch()
        dmp.Patch_Margin = context_lines

        files = list()
        for filename in filenames:
            patches = dmp.patch_make(a.get(filename, ''), b.get(filename, ''))
            text = dmp.patch_toText(patches)
            files.append((filename, text))

        return Protocol(data=files_to_proto(files))

    def apply_patch(self, patch):
        assert isinstance(patch, Protocol)

        a = dict(iter(self))
        b = dict(iter(patch))
        filenames = set(a.keys()).union(set(b.keys()))

        dmp = diff_match_patch()

        files = list()
        for filename in filenames:
            patches = dmp.patch_fromText(b.get(filename, ''))
            if patches:
                text = dmp.patch_apply(patches, a.get(filename, ''))
                files.append((filename, text))

        return Protocol(data=files_to_proto(files))

    def calculate_hash(self):
        hash_digest = blake2b_32(proto_to_bytes(self())).digest()
        return base58_encode(hash_digest, b'P').decode()
