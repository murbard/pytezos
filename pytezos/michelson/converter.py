from pytezos.michelson.micheline import Schema, collapse_micheline, build_maps, parse_micheline, make_json, \
    parse_json, make_micheline, is_micheline, michelson_to_micheline, BigMapSchema
from pytezos.michelson.formatter import micheline_to_michelson
from pytezos.michelson.docstring import generate_docstring


class MichelineSchemaError(ValueError):
    pass


def build_schema(code) -> Schema:
    """
    Creates internal structures necessary for decoding/encoding micheline:
    `metadata` -> micheline tree with collapsed `pair`, `or`, and `option` nodes
    `bin_types` -> maps binary path to primitive
    `bin_to_json` -> binary path to json path mapping
    `json_to_bin` -> reversed `bin_to_json`
    :param code: parameter or storage section of smart contract source code (in micheline)
    :return: Schema
    """
    try:
        metadata = collapse_micheline(code)
        return Schema(metadata, *build_maps(metadata))
    except (KeyError, ValueError, TypeError):
        raise MichelineSchemaError('Failed to build schema') from None


def decode_micheline(data, schema: Schema, root='0'):
    """
    Converts Micheline data into Python object
    :param data: Micheline expression
    :param schema: schema built for particular contract/section
    :param root: which binary node to take as root, used to decode BigMap values/diffs
    :return: Object
    """
    try:
        json_values = parse_micheline(data, schema.bin_to_json, schema.bin_types, root)
        return make_json(json_values)
    except (KeyError, IndexError, TypeError):
        print(generate_docstring(schema, 'schema'))
        raise MichelineSchemaError('Failed to decode micheline expression', data) from None


def encode_micheline(data, schema: Schema, root='0', binary=False):
    """
    Converts Python object into Micheline expression
    :param data: Python object
    :param schema: schema built for particular contract/section
    :param root: which binary node to take as root, used to encode BigMap values
    :param binary: Encode keys and addresses in bytes rather than strings, default is False
    :return: Micheline expression
    """
    try:
        json_root = schema.bin_to_json[root]
        bin_values = parse_json(data, schema.json_to_bin, schema.bin_types, json_root)
        return make_micheline(bin_values, schema.bin_types, root, binary)
    except (KeyError, IndexError, TypeError):
        print(generate_docstring(schema, 'schema'))
        raise MichelineSchemaError('Failed to encode micheline expression', data) from None


def convert(source, schema: Schema = None, output='micheline', inline=False):
    """
    Convert data between different representations (DO NOT USE FOR STORAGE/PARAMETER, can be ambiguous)
    :param source: Data, can be one of Michelson (string), Micheline expression, object
    :param schema: Needed if decoding/encoding objects (optional)
    :param output: Output format, one of 'micheline' (default), 'michelson', 'object'
    :param inline: Used for michelson output, whether to omit line breaks
    """
    if isinstance(source, str):
        try:
            source = michelson_to_micheline(source)
        except ValueError:
            assert schema
            source = encode_micheline(source, schema)
    elif not is_micheline(source):
        assert schema
        source = encode_micheline(source, schema)

    if output == 'michelson':
        return micheline_to_michelson(source, inline)
    elif output == 'object':
        assert schema
        return decode_micheline(source, schema)
    elif output == 'micheline':
        return source
    else:
        assert False, output


def build_big_map_schema(data, schema: Schema) -> BigMapSchema:
    bin_to_id = dict()
    id_to_bin = dict()

    def get_big_map_id(node, path):
        if len(path) == 0:
            assert node.get('int'), (node, path)
            return int(node['int'])
        else:
            assert node.get('args'), (node, path)
            return get_big_map_id(node['args'][int(path[0])], path[1:])

    for bin_path, prim in schema.bin_types.items():
        if prim == 'big_map':
            big_map_id = get_big_map_id(data, bin_path[1:])
            bin_to_id[bin_path], id_to_bin[big_map_id] = big_map_id, bin_path

    return BigMapSchema(bin_to_id, id_to_bin)
