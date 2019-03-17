import pendulum
from decimal import Decimal

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


def parse_item(value, prim):
    if prim in ['int', 'nat']:
        return int(value)
    if prim == 'timestamp':
        return pendulum.parse(value)
    if prim == 'mutez':
        return Decimal(value) / 10 ** 6
    return value


def parse_data(node):
    if isinstance(node, dict):
        args = map(parse_data, node.get('args', []))
        if node.get('prim') == 'Pair':
            res = flatten(tuple(args), tuple)
        elif node.get('prim') == 'Elt':
            res = list(args)
        else:
            res = next(v for _, v in node.items())
    elif isinstance(node, list):
        res = list(map(parse_data, node))
    else:
        raise NotImplementedError(node)

    return res


def parse_schema(node, path='0', parent=None):
    if node['prim'] == 'storage':
        return parse_schema(node['args'][0], parent=node)

    typename = next((a[1:] for a in node.get('annots', []) if a[0] == ':'), None)
    args = [
        parse_schema(arg, path=path + str(i), parent=node)
        for i, arg in enumerate(node.get('args', []))
    ]
    if node['prim'] == 'pair':
        if typename or parent is None or parent['prim'] != 'pair':
            args = flatten(args, list)
        else:
            return args

    res = dict(
        prim=node['prim'],
        path=path
    )
    if args:
        res['args'] = args

    fieldname = next((a[1:] for a in node.get('annots', []) if a[0] == '%'), typename)
    if fieldname:
        res['fieldname'] = fieldname

    return res


def apply_schema(data, schema):
    if schema['prim'] == 'storage':
        return apply_schema(data, schema['args'][0])

    if schema['prim'] == 'big_map':
        return {}

    if schema['prim'] == 'pair':
        values = [
            (arg.get('fieldname'), apply_schema(data[i], arg))
            for i, arg in enumerate(schema['args'])
        ]
        if all(map(lambda x: x[0], values)):
            return dict(values)
        else:
            return tuple(map(lambda x: x[1], values))

    if schema['prim'] == 'map':
        return {
            apply_schema(value[0], schema['args'][0]): apply_schema(value[1], schema['args'][1])
            for value in data
        }

    if schema['prim'] == 'set':
        return {
            apply_schema(value, schema['args'][0])
            for value in data
        }

    return parse_item(data, schema['prim'])


class Contract(RpcQuery):

    def __init__(self, *args, **kwargs):
        super(Contract, self).__init__(
            properties=[
                'balance', 'counter', 'delegatable', 'delegate', 'manager',
                'manager_key', 'script', 'spendable', 'storage'
            ],
            *args, **kwargs)

    @classmethod
    def from_json(cls, json):
        pass

    @classmethod
    def from_string(cls, text):
        pass

    @classmethod
    def from_file(cls, path):
        pass

    def raw_data(self):
        return parse_data(self.storage())

    def raw_schema(self):
        return parse_schema(self.script.get('code')[1])

    def data(self):
        script = self.get('script')
        data = parse_data(script['storage'])
        schema = parse_schema(script['code'][1])
        return apply_schema(data, schema)

