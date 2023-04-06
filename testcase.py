class TestCase:

    def __init__(self, test_query, condition_queries=None):
        if condition_queries is None:
            condition_queries = []
        self._test_query = test_query
        self._condition_queries = condition_queries

    def to_dict(self):
        return {
            'test_query': self._test_query.to_dict(),
            'condition_queries': [query.to_dict() for query in self._condition_queries]
        }
