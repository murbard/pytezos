class OperationResult:

    def __init__(self, **props):
        self.props = props
        for key, value in props.items():
            setattr(self, key, value)

    def __repr__(self):
        res = [
            super(OperationResult, self).__repr__(),
            '\nProperties',
            *list(map(lambda x: f'.{x}', self.props))
        ]
        return '\n'.join(res)

    @staticmethod
    def iter_contents(operation_group: dict):
        contents = operation_group.get('contents', [operation_group])
        for content in contents:
            yield {'internal': False, **content}
            internal_operation_results = content.get('metadata', {}).get('internal_operation_results', [])
            for result in internal_operation_results:
                yield {'internal': True, **result}

    @staticmethod
    def iter_results(operation_group: dict):
        for content in OperationResult.iter_contents(operation_group):
            if content['internal'] and content.get('result'):
                yield content['result']
            elif not content['internal'] and content.get('metadata', {}).get('operation_result'):
                yield content['metadata']['operation_result']

    @staticmethod
    def consumed_gas(operation_group):
        return sum(map(lambda x: int(x.get('consumed_gas', '0')),
                       OperationResult.iter_results(operation_group)))

    @staticmethod
    def paid_storage_size_diff(operation_group):
        return sum(map(lambda x: int(x.get('paid_storage_size_diff', '0')),
                       OperationResult.iter_results(operation_group)))

    @staticmethod
    def is_applied(operation_group):
        return all(map(lambda x: x['status'] == 'applied',
                       OperationResult.iter_results(operation_group)))

    @staticmethod
    def errors(operation_group: dict):
        for result in OperationResult.iter_results(operation_group):
            if result['status'] == 'failed':
                return result['errors']

    @staticmethod
    def originated_contracts(operation_group: dict):
        originated_contracts = list()
        for result in OperationResult.iter_results(operation_group):
            originated_contracts.extend(result.get('originated_contracts', []))
        return originated_contracts

    @staticmethod
    def get_operation(operation_group: dict, **predicates):
        def match(x):
            return all(map(lambda pred: x.get(pred[0]) == pred[1], predicates.items()))

        if not predicates:
            assert len(operation_group['contents']) == 1
            return operation_group['contents'][0]
        else:
            contents = list(filter(match, OperationResult.iter_contents(operation_group)))
            assert len(contents) == 1, operation_group
            return contents[0]

    @classmethod
    def from_transaction(cls, operation_group: dict, **predicates):
        if not cls.is_applied(operation_group):
            raise ValueError(cls.errors(operation_group))

        operation = cls.get_operation(operation_group, kind='transaction', **predicates)
        if operation.get('metadata'):
            operation_result = operation['metadata']['operation_result']
        elif operation.get('result'):
            operation_result = operation['result']
        else:
            operation_result = {}

        return cls(
            parameters=operation.get('parameters'),
            storage=operation_result.get('storage'),
            big_map_diff=operation_result.get('big_map_diff', [])
        )
