import re
from pprint import pformat
from typing import List

from pytezos.repl.types import StackItem, assert_stack_item
from pytezos.michelson.converter import micheline_to_michelson


class Context:

    def __init__(self, stack=None):
        self.stack = stack or []
        self.meta = dict()
        self.stdout = list()
        self.depth = 0

    def ins_many(self, items: list, index: int = 0):
        assert len(self.stack) >= index, f'got {len(self.stack)} items, wanted to insert before {index}th'
        for item in items:
            assert_stack_item(item)
        self.stack[index:index] = items
        self.print(f' push {len(items)} items;')

    def ins(self, item: StackItem, index: int = 0, annots=None):
        assert_stack_item(item)
        self.stack.insert(index, item.rename(annots))
        self.print(f' push {repr(item)};')

    def peek(self, index=0):
        assert len(self.stack) > 0, 'stack is empty'
        assert index < len(self.stack), f'requested {index}th element, got only {len(self.stack)} items'
        return self.stack[index]

    def pop_many(self, count: int, index: int = 0) -> List[StackItem]:
        assert len(self.stack) - index >= count, f'got {len(self.stack)} items, requested {count} from {index}th'
        self.print(f' pop {count} item{"s" if count > 1 else ""};')
        return [self.stack.pop(index) for _ in range(count)]

    def pop(self, index: int = 0):
        res = self.pop_many(count=1, index=index)
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
            indent = '  ' * self.depth
            self.print(f'\n{indent}{prim}:')
        self.depth += 1

    def end(self):
        self.depth -= 1

    def __len__(self) -> int:
        return len(self.stack)

    def __repr__(self):
        return pformat(self.stack)
