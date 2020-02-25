import re
from pprint import pformat
from typing import List

from pytezos.repl.types import StackItem, assert_stack_item
from pytezos.michelson.converter import micheline_to_michelson


class Context:

    def __init__(self, stack=None):
        self.stack = stack or []
        self.protected = 0
        self.meta = dict()
        self.stdout = list()
        self.exec_depth = 0

    def protect(self, count: int):
        assert len(self.stack) >= count, f'got {len(self.stack)} items, wanted to protect {count}'
        self.protected += count
        self.print(f' protect {count} items;')

    def restore(self, count: int):
        assert self.protected >= count, f'wanted to restore {count}, only {self.protected} protected'
        self.print(f' restore {count} items;')
        self.protected -= count

    def push_many(self, *items):
        _ = list(map(assert_stack_item, items))
        self.stack[self.protected:self.protected] = items
        if len(items) <= 3:
            body = ', '.join(map(repr, items))
        else:
            body = f'{len(items)} items'
        self.print(f' push {body}')

    def push(self, item: StackItem, annots=None):
        assert_stack_item(item)
        self.stack.insert(self.protected, item.rename(annots))
        self.print(f' push {repr(item)};')

    def peek(self):
        assert len(self.stack) > 0, 'stack is empty'
        return self.stack[0]

    def pop_many(self, count: int) -> List[StackItem]:
        assert len(self.stack) - self.protected >= count, \
            f'got {len(self.stack) - self.protected} items, requested {count} '
        res = [self.stack.pop(self.protected) for _ in range(count)]
        if count <= 3:
            body = ', '.join(map(repr, res))
        else:
            body = f'{count} items'
        self.print(f' pop {body};')
        return res

    def pop(self):
        res = self.pop_many(count=1)
        return res[0]

    def pop2(self):
        return tuple(self.pop_many(count=2))

    def pop3(self):
        return tuple(self.pop_many(count=3))

    def get(self, key, default=None):
        return self.meta.get(key, default)

    def set(self, key, value):
        self.meta[key] = value
        if key in ['parameter', 'storage', 'code']:
            val = micheline_to_michelson(value, inline=True)
        else:
            val = repr(value)
        self.print(f' set {key}={val};')

    def unset(self, key):
        del self.meta[key]
        self.print(f' unset {key};')

    def drop_all(self):
        self.stack.clear()
        self.print(f' drop all;')

    def dump(self, count: int):
        count = min(count, len(self.stack))
        return self.stack[:count]

    def print(self, template: str):
        def format_stack_item(match):
            i = int(match.groups()[0])
            assert i < len(self.stack), f'requested {i}th element, got only {len(self.stack)} items'
            return repr(self.stack[i])

        message = re.sub(r'\{(\d+)\}', format_stack_item, template)
        self.stdout.append(message)

    def begin(self, prim=None):
        if prim:
            indent = '  ' * self.exec_depth
            self.print(f'\n{indent}{prim}:')
        self.exec_depth += 1

    def end(self):
        self.exec_depth -= 1

    def __len__(self) -> int:
        return len(self.stack)

    def __repr__(self):
        return pformat(self.stack)
