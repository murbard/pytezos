from pprint import pformat
from typing import List

from pytezos.repl.types import StackItem, assert_stack_item
from pytezos.repl.parser import assert_pushable


class Stack:

    def __init__(self, items: list):
        self.items = items

    def ins_many(self, items: list, index: int = 0):
        assert len(self.items) >= index, f'got {len(self.items)} items, wanted to insert before {index}th'
        for item in items:
            assert_stack_item(item)
            assert_pushable(item.type_expr)
        self.items[index:index] = items

    def ins(self, item: StackItem, index: int = 0, annots=None):
        assert_stack_item(item)
        assert_pushable(item.type_expr)
        self.items.insert(index, item.rename(annots))
        if index == 0:
            return self.items[index]

    def peek(self):
        assert len(self.items) > 0, 'stack is empty'
        return self.items[0]

    def pop_many(self, count: int, index: int = 0) -> List[StackItem]:
        assert len(self.items) - index >= count, f'got {len(self.items)} items, requested {count} from {index}th'
        return [self.items.pop(index) for _ in range(count)]

    def pop(self, index: int = 0):
        res = self.pop_many(count=1, index=index)
        return res[0]

    def pop2(self):
        return tuple(self.pop_many(count=2))

    def pop3(self):
        return tuple(self.pop_many(count=3))

    def __len__(self) -> int:
        return len(self.items)

    def __repr__(self):
        return pformat(self.items)
