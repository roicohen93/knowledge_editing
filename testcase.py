class TestCase:

    def __init__(self, fact, test_query, condition_queries=None):
        self._fact = fact
        self._test_query = test_query
        if condition_queries is None:
            condition_queries = []
        self._condition_queries = condition_queries

    def get_fact(self):
        return self._fact

    def get_test_query(self):
        return self._test_query

    def get_condition_queries(self):
        return self._condition_queries

    def to_dict(self):
        return {
            'fact:': self._fact.to_dict(),
            'test_query': self._test_query.to_dict(),
            'condition_queries': [query.to_dict() for query in self._condition_queries]
        }
