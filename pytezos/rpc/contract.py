import pendulum
from decimal import Decimal
from collections import namedtuple

from pytezos.rpc.node import RpcQuery
from pytezos.encoding import base58_encode
from pytezos.michelson import MichelsonParser

Schema = namedtuple('Schema', ['type_map', 'collapsed_tree'])
michelson_parser = MichelsonParser()


def flatten(items, itemtype):
    if isinstance(items, itemtype):
        if len(items) == 0:
            return itemtype()
        first, rest = items[0], items[1:]
        return flatten(first, itemtype) + flatten(rest, itemtype)
    else:
        return itemtype([items])


def make_dict(**kwargs) -> dict:
    return {k: v for k, v in kwargs.items() if v}


def decode_literal(node, prim):
    raw_type, value = next(iter(node.items()))
    if prim in ['int', 'nat']:
        return int(value)
    if prim == 'timestamp':
        if raw_type == 'int':
            return pendulum.from_timestamp(value)
        else:
            return pendulum.parse(value)
    if prim == 'mutez':
        return Decimal(value) / 10 ** 6
    if prim == 'bool':
        return value == 'True'
    if prim == 'address' and raw_type == 'bytes':
        prefix = {'00': b'tz1', '01': b'tz2', '02': b'tz3'}  # TODO: check
        return base58_encode(bytes.fromhex(value[2:]), prefix[value[:2]])
    return value


def encode_literal(value, prim):
    if not isinstance(value, str):
        if prim in ['int', 'nat']:
            value = str(value)
        elif prim == 'timestamp':
            if isinstance(value, int):
                value = pendulum.from_timestamp(value)
            if isinstance(value, pendulum.DateTime):
                value = value.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif prim == 'mutez':
            if isinstance(value, Decimal):
                value = int(value * 10 ** 6)
            if isinstance(value, int):
                value = str(value)
        elif prim == 'bool':
            value = True if value else False
        else:
            value = str(value)

    return {prim: value}


def parse_schema(code) -> Schema:
    type_map = dict()

    def get_annotation(x, prefix, default=None):
        return next((a[1:] for a in x.get('annots', []) if a[0] == prefix), default)

    def parse_node(node, path='0', nested=None):
        if node['prim'] in ['storage', 'parameter']:
            return parse_node(node['args'][0])

        type_map[path] = dict(prim=node['prim'])
        typename = get_annotation(node, ':')

        args = [
            parse_node(arg, path=path + str(i), nested=node['prim'])
            for i, arg in enumerate(node.get('args', []))
        ]

        if node['prim'] in ['pair', 'or']:
            if typename or nested != node['prim']:
                args = flatten(args, list)  # TODO: pair/or conflicts?
                props = list(map(lambda x: x.get('name'), args))
                if all(props):
                    type_map[path]['props'] = props
            else:
                return args

        return make_dict(
            prim=node['prim'],
            path=path,
            args=args,
            name=get_annotation(node, '%', typename),
        )

    collapsed_tree = parse_node(code)
    return Schema(type_map, collapsed_tree)


def decode_data(data, schema: Schema, annotations=True, literals=True):
    def decode_node(node, path='0'):
        type_info = schema.type_map.get(path, {})
        if isinstance(node, dict):
            args = (
                decode_node(arg, path + str(i))
                for i, arg in enumerate(node.get('args', []))
            )
            if node.get('prim') == 'Pair':
                res = flatten(tuple(args), tuple)
                if type_info.get('props') and annotations:
                    res = dict(zip(type_info['props'], res))
            elif node.get('prim') == 'Elt':
                res = list(args)
            elif node.get('prim') == 'Left':
                res = next(iter(args))
            elif node.get('prim') == 'Right':
                res = decode_node(node['args'][0], path + '1')
            elif node.get('prim') == 'Some':
                res = next(iter(args))
            elif node.get('prim') == 'None':
                res = None
            elif literals:
                res = decode_literal(node, type_info['prim'])
            else:
                _, res = next(iter(node.items()))

        elif isinstance(node, list):
            if type_info['prim'] in ['map', 'big_map']:
                res = dict(decode_node(item, path) for item in node)
            else:
                args = (decode_node(item, path + '0') for item in node)
                if type_info['prim'] == 'set':
                    res = set(args)
                elif type_info['prim'] == 'list':
                    res = list(args)
                else:
                    raise ValueError(node, type_info)
        else:
            raise ValueError(node, type_info)

        return res

    return decode_node(data)


def build_value_map(data, schema: Schema) -> dict:
    value_map = dict()

    def parse_value(node, node_info, is_element=False):
        if node_info['prim'] == 'pair':
            values = node
            if isinstance(node, dict):  # props
                values = [node[arg['name']] for arg in node_info['args']]
            for i, arg_info in enumerate(node_info['args']):
                parse_value(values[i], arg_info, is_element)

        elif node_info['prim'] in ['map', 'big_map']:
            for key, value in node.items():
                parse_value(key, node_info['args'][0], True)
                parse_value(value, node_info['args'][1], True)

        elif node_info['prim'] in ['set', 'list']:
            for value in node:
                parse_value(value, node_info['args'][0], True)

        elif node_info['prim'] == 'or':
            pass  # TODO

        elif node_info['prim'] == 'contract':
            pass

        elif is_element:
            value_map[node_info['path']] = value_map.get(node_info['path'], []) + [node]
        else:
            value_map[node_info['path']] = node

    parse_value(data, schema.collapsed_tree)
    return value_map


def encode_data(data, schema: Schema):
    value_map = build_value_map(data, schema)

    def encode_node(path='0', index=None):
        def get_value(suffix=''):
            v = value_map.get(path + suffix)
            if index is not None:
                return v[index]
            return v

        type_info = schema.type_map[path]
        if type_info['prim'] == 'pair':
            return dict(
                prim='Pair',
                args=list(map(lambda x: encode_node(path + x, index), '01'))
            )
        elif type_info['prim'] in ['map', 'big_map']:
            return [
                dict(
                    prim='Elt',
                    args=[encode_node(path + '0', i), encode_node(path + '1', i)]
                )
                for i in range(len(get_value('0')))
            ]
        elif type_info['prim'] in ['set', 'list']:
            return [
                encode_node(path + '0', i)
                for i in range(len(get_value('0')))
            ]
        elif type_info['prim'] == 'or':
            pass
        elif type_info['prim'] == 'optional':
            if get_value('0') is None:
                return dict(prim='None')
            else:
                return dict(
                    prim='Some',
                    args=[encode_node(path + '0', index)]
                )

        return encode_literal(get_value(), type_info['prim'])

    return encode_node()


class Contract(RpcQuery):

    def __init__(self, code=None, *args, **kwargs):
        super(Contract, self).__init__(
            properties=[
                'balance', 'counter', 'delegatable', 'delegate', 'manager',
                'manager_key', 'script', 'spendable', 'storage'
            ],
            *args, **kwargs)
        self._code = code

    def _get_code(self):
        if self._code:
            return self._code
        return self.get('script')['code']

    def _get_section(self, section):
        code = self._get_code()
        return next(s for s in code if s['prim'] == section)

    def _get_schema(self, section):
        return parse_schema(self._get_section(section))

    @classmethod
    def from_code(cls, code):
        return Contract(code=code)

    @classmethod
    def from_string(cls, text):
        code = michelson_parser.parse(text)
        return cls.from_code(code)

    @classmethod
    def from_file(cls, path):
        with open(path) as f:
            return cls.from_string(f.read())

    def decode_storage(self, annotations=True, literals=True):
        script = self.get('script')
        return decode_data(
            data=script['storage'],
            schema=self._get_schema('storage'),
            annotations=annotations,
            literals=literals
        )

    def encode_storage(self, data):
        return encode_data(
            data=data,
            schema=self._get_schema('storage')
        )
