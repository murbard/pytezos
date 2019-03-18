import pendulum
from decimal import Decimal
from functools import lru_cache

from pytezos.rpc.node import RpcQuery
from pytezos.michelson import MichelsonParser


def flatten(items, itemtype):
    if isinstance(items, itemtype):
        if len(items) == 0:
            return itemtype()
        first, rest = items[0], items[1:]
        return flatten(first, itemtype) + flatten(rest, itemtype)
    else:
        return itemtype([items])


def decode_item(value, prim):
    if prim in ['int', 'nat']:
        return int(value)
    if prim == 'timestamp':
        return pendulum.parse(value)
    if prim == 'mutez':
        return Decimal(value) / 10 ** 6
    if prim == 'bool':
        return value == 'True'
    return value


def encode_item(value, prim):
    return {prim: value}


def get_annot(x, prefix, default=None):
    return next((a[1:] for a in x.get('annots', []) if a[0] == prefix), default)


def make_dict(**kwargs) -> dict:
    return {k: v for k, v in kwargs.items() if v}


def make_storage_schema(code) -> tuple:
    decode_map = dict()

    def parse_code(node, path='0', nested_pair=False):
        if node['prim'] == 'storage':
            return parse_code(node['args'][0])

        decode_map[path] = dict(prim=node['prim'])
        is_pair = node['prim'] == 'pair'
        typename = get_annot(node, ':')

        args = [
            parse_code(arg, path=path + str(i), nested_pair=is_pair)
            for i, arg in enumerate(node.get('args', []))
        ]

        if is_pair:
            if typename or not nested_pair:
                args = flatten(args, list)
                props = list(map(lambda x: x.get('name'), args))
                if all(props):
                    decode_map[path]['props'] = props
            else:
                return args

        return make_dict(
            prim=node['prim'],
            level=len(path),
            args=args,
            name=get_annot(node, '%', typename),
        )

    encode_map = parse_code(code)
    return decode_map, encode_map


def decode_storage(node, schema: dict, path='0'):
    info = schema.get(path, {})
    if isinstance(node, dict):
        args = (
            decode_storage(arg, schema, path + str(i))
            for i, arg in enumerate(node.get('args', []))
        )
        if node.get('prim') == 'Pair':
            res = flatten(tuple(args), tuple)
            if info.get('props'):
                res = dict(zip(info['props'], res))
        elif node.get('prim') == 'Elt':
            res = list(args)
        else:
            res = decode_item(next(v for _, v in node.items()), info['prim'])
    elif isinstance(node, list):
        if info['prim'] == 'map':
            res = {
                decode_storage(item['args'][0], schema, path + '0'):
                    decode_storage(item['args'][1], schema, path + '1')
                for item in node
            }
        elif info['prim'] == 'set':
            res = {
                decode_storage(item, schema, path + '0')
                for item in node
            }
        elif info['prim'] == 'list':
            res = [
                decode_storage(item, schema, path + '0')
                for item in node
            ]
        else:
            raise NotImplementedError(node, info)
    else:
        raise NotImplementedError(node, info)

    return res


def make_pair(args):
    pair = dict(prim='Pair')
    step = args[1]['level'] - args[0]['level']
    if step == 0:
        pair['args'] = list(map(lambda x: x['value'], args[:2]))
    elif step == 1:
        pair['args'] = [args[0]['value'], make_pair(args[1:])]
    else:
        pair['args'] = [make_pair(args[:step]), make_pair(args[step:])]
    return pair


def encode_storage(data, schema):
    if schema['prim'] == 'pair':
        values = data
        if isinstance(values, dict):
            values = [values[arg['name']] for arg in schema['args']]

        args = [
            dict(level=schema['args'][i]['level'], value=encode_storage(item, schema['args'][i]))
            for i, item in enumerate(values)
        ]
        res = make_pair(args)
    elif schema['prim'] == 'map':
        res = [
            dict(
                prim='Elt',
                args=[encode_storage(key, schema['args'][0]), encode_storage(value, schema['args'][1])]
            )
            for key, value in data.items()
        ]
    elif schema['prim'] == 'set':
        res = [
            encode_storage(item, schema['args'][0])
            for item in data
        ]
    elif schema['prim'] == 'big_map':
        res = []
    else:
        res = encode_item(data, schema['prim'])

    return res


class Contract(RpcQuery):

    def __init__(self, *args, **kwargs):
        super(Contract, self).__init__(
            properties=[
                'balance', 'counter', 'delegatable', 'delegate', 'manager',
                'manager_key', 'script', 'spendable', 'storage'
            ],
            *args, **kwargs)

    @lru_cache(maxsize=None)
    def _get_schema(self):
        code = self.script.get('code')
        storage_section = next(s for s in code if s['prim'] == 'storage')
        return make_storage_schema(storage_section)

    @classmethod
    def from_json(cls, json):
        pass

    @classmethod
    def from_string(cls, text):
        pass

    @classmethod
    def from_file(cls, path):
        pass

    def data(self):
        script = self.get('script')
        schema = self._get_schema()[0]
        return decode_storage(script['storage'], schema)
