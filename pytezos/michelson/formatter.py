line_size = 100


def is_framed(node):
    if node['prim'] in {'Pair', 'Left', 'Right', 'Some',
                        'pair', 'or', 'option', 'map', 'big_map', 'list', 'set', 'contract', 'lambda'}:
        return True
    elif node['prim'] in {'key', 'unit', 'signature', 'operation',
                          'int', 'nat', 'string', 'bytes', 'mutez', 'bool', 'key_hash', 'timestamp', 'address'}:
        return 'annots' in node
    return False


def is_complex(node):
    return node['prim'] == 'LAMBDA' \
           or node['prim'].startswith('IF')


def is_inline(node):
    return node['prim'] == 'PUSH'


def format_node(node, indent='', inline=False):
    if isinstance(node, list):
        seq_indent = indent + ' ' * 2
        items = list(map(lambda x: format_node(x, seq_indent, inline), node))
        length = len(indent) + sum(map(len, items)) + 4
        if inline or length < line_size:
            seq = ' ; '.join(items)
        else:
            seq = f' ;\n{seq_indent}'.join(items)
        return f'{{ {seq} }}'

    elif isinstance(node, dict):
        if node.get('prim'):
            expr = ' '.join([node['prim']] + node.get('annots', []))
            args = node.get('args', [])

            if is_complex(node):
                arg_indent = indent + ' ' * 2
                items = list(map(lambda x: format_node(x, arg_indent, inline), args))
                length = len(indent) + len(expr) + sum(map(len, items)) + len(items) + 1
                if inline or length < line_size:
                    expr = f'{expr} {" ".join(items)}'
                else:
                    expr = f'\n{arg_indent}'.join([expr] + items)

            elif len(args) == 1:
                arg_indent = indent + ' ' * (len(expr) + 1)
                expr = f'{expr} {format_node(args[0], arg_indent, inline)}'

            elif len(args) > 1:
                arg_indent = indent + ' ' * 2
                alt_indent = indent + ' ' * (len(expr) + 2)
                for arg in args:
                    item = format_node(arg, arg_indent, inline)
                    length = len(indent) + len(expr) + len(item) + 1
                    if inline or is_inline(node) or length < line_size:
                        arg_indent = alt_indent
                        expr = f'{expr} {item}'
                    else:
                        expr = f'{expr}\n{arg_indent}{item}'

            return f'({expr})' if is_framed(node) else expr
        else:
            assert len(node) == 1
            value = next(iter(node.values()))
            return value if value.isdigit() else f'"{value}"'
    else:
        assert False, node
