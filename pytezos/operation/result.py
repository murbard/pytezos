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

    @classmethod
    def get_operation(cls, operation_group: dict, **predicates):
        def match(x):
            return all(map(lambda pred: x.get(pred[0]) == pred[1], predicates.items()))

        if not predicates:
            assert len(operation_group['contents']) == 1
            return operation_group['contents'][0]
        else:
            contents = list()
            for content in operation_group['contents']:
                if match(content):
                    contents.append(content)
                else:
                    try:
                        contents.extend(list(filter(match, content['metadata']['internal_operation_results'])))
                    except (KeyError, TypeError):
                        pass
            assert len(contents) == 1, operation_group
            return contents[0]

    @classmethod
    def from_transaction(cls, operation_group: dict, **predicates):
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
