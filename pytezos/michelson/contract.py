from pytezos.michelson import michelson_to_micheline
from pytezos.michelson.coding import build_schema, decode_micheline, encode_micheline

# Binary path for type map
# TODO: In Babylon there can be more than one Big Map
BIG_MAP_KEY = '00'
BIG_MAP_VAL = '01'



#
# def decode_schema(schema: Schema):
#     def decode_node(node):
#         if node['prim'] == 'or':
#             return {
#                 arg.get('name', str(i)): decode_node(arg)
#                 for i, arg in enumerate(node['args'])
#             }
#         if node['prim'] == 'pair':
#             args = list(map(lambda x: (x.get('name'), decode_node(x)), node['args']))
#             names, values = zip(*args)
#             return dict(args) if all(names) else values
#         if node['prim'] == 'set':
#             return {decode_node(node['args'][0])}
#         if node['prim'] == 'list':
#             return [decode_node(node['args'][0])]
#         if node['prim'] in {'map', 'big_map'}:
#             return {decode_node(node['args'][0]): decode_node(node['args'][1])}
#         if node['prim'] == 'option':
#             return decode_node(node['args'][0])
#
#         return f'#{node["prim"]}'
#
#     return decode_node(schema.collapsed_tree)


class Contract:

    def __init__(self, code: list):
        """
        :param code: [{'prim': 'parameter'}, {'prim': 'storage'}, {'prim': 'code'}]
        """
        self.code = code
        self.schema = {
            section: build_schema(next(x for x in code if x['prim'] == section))
            for section in ['parameter', 'storage']
        }

    @classmethod
    def from_micheline(cls, code):
        return cls(code)

    @classmethod
    def from_michelson(cls, source):
        return cls(michelson_to_micheline(source))

    @classmethod
    def from_file(cls, path):
        with open(path) as f:
            return cls.from_michelson(f.read())

    def convert(self, data, section, output):
        if output == 'michel':
            return encode_data(data, self.schema[section])
        elif output == 'micheline':
            return decode_data(data, self.schema[section])
        else:
            raise NotImplementedError(output)

    def entries(self):
        pass



    # def big_map_query(self, key):
    #     schema = self.schema['storage']
    #     return dict(
    #         key=encode_data(key, schema, root=BIG_MAP_KEY),
    #         type=schema.type_map[BIG_MAP_KEY]
    #     )
    #
    # def big_map_decode(self, val):
    #     schema = self.schema['storage']
    #     return decode_data(val, schema, root=BIG_MAP_VAL)
    #
    # def big_map_diff_decode(self, diff):
    #     schema = self.schema['storage']
    #     return {
    #         decode_data(item['key'], schema, root=BIG_MAP_KEY):
    #             decode_data(item['value'], schema, root=BIG_MAP_VAL)
    #         for item in diff
    #     }
