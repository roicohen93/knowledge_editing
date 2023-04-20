from enum import Enum, auto


class TestResult(Enum):
    NOT_EXECUTED = auto()
    PASSED = auto()
    FAILED = auto()


class TestRunner:

    def __init__(self, query_executor, model_editor):
        self._query_executor = query_executor
        self._model_editor = model_editor

    def run_testcases(self, fact, test_cases):
        # Modify model
        modified_query_executor = self._query_executor.copy()
        edited_model = self._model_editor.edit_model(modified_query_executor.get_model(),
                                                     modified_query_executor.get_tokenizer(),
                                                     fact)
        modified_query_executor.set_model(edited_model)

        # Test edit
        if not modified_query_executor.execute_query(fact.get_fact_query()):
            return False, {}

        # Run tests
        results = {TestResult.NOT_EXECUTED: [], TestResult.PASSED: [], TestResult.FAILED: []}
        for test_case in test_cases:
            # Check conditions
            for condition_query in test_case.get_condition_queries():
                if not self._query_executor.execute_query(condition_query):
                    results[TestResult.NOT_EXECUTED].append(test_case)
                    break

            # Test modified model
            if test_case not in results[TestResult.NOT_EXECUTED]:
                if modified_query_executor.execute_query(test_case.get_test_query()):
                    results[TestResult.PASSED].append(test_case)
                else:
                    results[TestResult.FAILED].append(test_case)

        return True, results


if __name__ == '__main__':
    from queryexecutor import GPT2QueryExecutor
    from modeleditor import MEMITModelEditor, ROMEModelEditor, MENDModelEditor
    from fact import Fact
    from relation import Relation
    from query import Query
    from testcase import TestCase

    f = Fact('Q76', Relation.FATHER, 'Q12379')  # Barack Obama's father is Mario
    tq = Query('Q76', Relation.UNCLE, ['Q210593'])  # Barack Obama's uncle is Luigi
    cq = Query('Q12379', Relation.BROTHER, ['Q210593'])  # Mario's brother is Luigi
    tc = TestCase(tq, [cq])
    tr = TestRunner(GPT2QueryExecutor(model_size='xl'), ROMEModelEditor('gpt2-xl'))
    res = tr.run_testcases(f, [tc])
    print(res)
