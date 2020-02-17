from pprint import pformat
from typing import List

from pytezos.repl.types import StackItem, assert_stack_item


class Context:

    def __init__(self, stack: list):
        self.stack = stack
        self.meta = dict()

    def ins_many(self, items: list, index: int = 0):
        assert len(self.stack) >= index, f'got {len(self.stack)} items, wanted to insert before {index}th'
        for item in items:
            assert_stack_item(item)
        self.stack[index:index] = items

    def ins(self, item: StackItem, index: int = 0, annots=None):
        assert_stack_item(item)
        self.stack.insert(index, item.rename(annots))
        if index == 0:
            return self.stack[index]

    def peek(self, index=0):
        assert len(self.stack) > 0, 'stack is empty'
        assert index < len(self.stack), f'requested {index}th element, got only {len(self.stack)} items'
        return self.stack[index]

    def pop_many(self, count: int, index: int = 0) -> List[StackItem]:
        assert len(self.stack) - index >= count, f'got {len(self.stack)} items, requested {count} from {index}th'
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

    def drop_all(self):
        self.stack.clear()

    def __len__(self) -> int:
        return len(self.stack)

    def __repr__(self):
        return pformat(self.stack)
