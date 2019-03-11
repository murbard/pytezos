from typing import Any, Callable, Generator
from loguru import logger

from pytezos.rpc.chain import Chain
from pytezos.rpc.operation import Operation


def find_state_change_intervals(head: int, tail: int, get: Callable, equals: Callable,
                                step=60) -> Generator:
    succ_value = get(head)

    for level in range(head - step, tail, -step):
        value = get(level)
        logger.debug(f'{value} at level {level}')

        if not equals(value, succ_value):
            yield level + step, succ_value, level, value
            succ_value = value


def find_state_change(head: int, tail: int, get: Callable, equals: Callable,
                      pred_value: Any) -> (int, Any):
    def bisect(start: int, end: int):
        if end == start + 1:
            return end, get(end)

        level = (end + start) // 2
        value = get(level)
        logger.debug(f'{value} at level {level}')

        if equals(value, pred_value):
            return bisect(level, end)
        else:
            return bisect(start, level)

    return bisect(tail, head)


def walk_state_change_interval(head: int, tail: int, get: Callable, equals: Callable,
                               head_value: Any, tail_value: Any) -> Generator:
    level = tail
    value = tail_value
    while not equals(value, head_value):
        level, value = find_state_change(
            head, level, get, equals,
            pred_value=value)
        yield level, value


def find_state_changes(head: int, tail: int, get: Callable, equals: Callable) -> Generator:
    for int_head, int_head_value, int_tail, int_tail_value in find_state_change_intervals(
            head, tail, get, equals):
        for change in walk_state_change_interval(
                int_head, int_tail, get, equals,
                head_value=int_head_value,
                tail_value=int_tail_value):
            yield change


class SearchChain(Chain):

    @classmethod
    def from_chain(cls, chain: Chain):
        return SearchChain(
            path=chain._path,
            node=chain._node,
            **chain._kwargs
        )

    def get_voting_period(self):
        level_info = self.head.metadata.get('level')
        head = level_info['level']
        tail = head - level_info['voting_period_position']
        return head, tail

    def find_proposal_inject_level(self, proposal_id) -> int:
        level, _ = find_state_change(
            *self.get_voting_period(),
            get=lambda x: self.blocks[x].votes.roll_count(proposal_id),
            equals=lambda x, y: x == y,
            pred_value=0
        )
        return level

    def find_proposal_votes_levels(self, proposal_id) -> Generator:
        for level, _ in find_state_changes(
                *self.get_voting_period(),
                get=lambda x: self.blocks[x].votes.roll_count(proposal_id),
                equals=lambda x, y: x == y):
            yield level

    def find_proposal_inject_operation(self, proposal_id) -> Operation:
        level = self.find_proposal_inject_level(proposal_id)
        operations = self.blocks[level].operations.votes()
        if not operations:
            raise ValueError('Injection operation not found.')

        return Operation.from_data(operations[0])

    def find_proposal_votes_operations(self, proposal_id) -> Generator:
        for level in self.find_proposal_votes_levels(proposal_id):
            for operation in self.blocks[level].operations.votes():
                yield Operation.from_data(operation)
