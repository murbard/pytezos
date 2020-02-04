from copy import deepcopy


class Stack:

    def __init__(self, items: list):
        self.items = items

    def ins_many(self, items: list, index: int = 0):
        assert len(self.items) >= index, f'Got {len(self.items)} items, wanted to insert before {index}th'
        self.items[index:index] = items

    def ins(self, item: object, index: int = 0):
        self.ins_many([item], index=index)

    def peek(self) -> object:
        assert len(self.items) > 0, 'Stack is empty'
        return self.items[0]

    def pop_many(self, count: int, index: int = 0) -> list:
        assert len(self.items) - index >= count, f'Got {len(self.items)} items, requested {count} from {index}th'
        return [self.items.pop(index=index) for _ in range(count)]

    def pop(self, index: int = 0) -> object:
        return self.pop_many(count=1, index=index)[0]

    def pop2(self) -> list:
        return self.pop_many(count=2)

    def pop3(self) -> list:
        return self.pop_many(count=3)

    def copy(self) -> 'Stack':
        return Stack(deepcopy(self.items))

    def __len__(self):
        return len(self.items)
