from enum import Enum, auto

from benchmark import RecentlyAddedExample, CounterFactualExample


class TestResult(Enum):
    NOT_EXECUTED = auto()
    PASSED = auto()
    FAILED = auto()


class ExampleResult(Enum):
    EXECUTED = auto()
    EDIT_FAILED = auto()
    NEW_FACT_KNOWN = auto()
    PREV_FACT_UNKNOWN = auto()


class TestRunner:

    def __init__(self, query_executor, model_editor):
        self._query_executor = query_executor
        self._model_editor = model_editor

    def run_testcases(self, example, test_cases):
        example_result = ExampleResult.EXECUTED
        test_results = {TestResult.NOT_EXECUTED: [], TestResult.PASSED: [], TestResult.FAILED: []}

        # Check testcase conditions
        for test_case in test_cases:
            for condition_query in test_case.get_condition_queries():
                if not self._query_executor.execute_query(condition_query):
                    test_results[TestResult.NOT_EXECUTED].append(test_case)
                    break

        # Check if fact is known/unknown according to example type
        if isinstance(example, RecentlyAddedExample):
            if self._query_executor.execute_query(example.fact.get_fact_query()):
                example_result = ExampleResult.NEW_FACT_KNOWN
        elif isinstance(example, CounterFactualExample):
            if not self._query_executor.execute_query(example.previous_fact.get_fact_query()):
                example_result = ExampleResult.PREV_FACT_UNKNOWN

        # Modify model
        self._model_editor.edit_model(example.fact)

        # Test edit
        if not self._query_executor.execute_query(example.fact.get_fact_query()):
            example_result = ExampleResult.EDIT_FAILED

        # Test modified model
        for test_case in test_cases:
            if test_case not in test_results[TestResult.NOT_EXECUTED]:
                test_case_results = [self._query_executor.execute_query(test_query)
                                     for test_query in test_case.get_test_queries()]
                if test_case.get_test_condition() == TestCase.OR_TEST_CONDITION and True in test_case_results:
                    test_results[TestResult.PASSED].append(test_case)
                elif test_case.get_test_condition() == TestCase.AND_TEST_CONDITION and False not in test_case_results:
                    test_results[TestResult.PASSED].append(test_case)
                else:
                    test_results[TestResult.FAILED].append(test_case)

        # Restore model
        self._model_editor.restore_model()

        return example_result, test_results


if __name__ == '__main__':
    from queryexecutor import GPT2QueryExecutor
    from modeleditor import MEMITModelEditor, ROMEModelEditor, MENDModelEditor
    from fact import Fact
    from relation import Relation
    from query import Query
    from testcase import TestCase

    f = Fact('Q76', Relation.FATHER, 'Q12379')  # Barack Obama's father is Mario
    f_prev = Fact('Q76', Relation.FATHER, 'Q649593')  # Barack Obama's father is Barack Obama Sr.
    e = CounterFactualExample(f, f_prev)
    # e = RecentlyAddedExample(f)
    tq = Query('Q76', Relation.UNCLE, ['Q210593'])  # Barack Obama's uncle is Luigi
    cq = Query('Q12379', Relation.BROTHER, ['Q210593'])  # Mario's brother is Luigi
    tc = TestCase(tq, [cq])
    qe = GPT2QueryExecutor(model_size='medium')
    me = ROMEModelEditor(qe)
    tr = TestRunner(qe, me)
    res = tr.run_testcases(e, [tc])
    print('------')
    print(f)
    print(tc)
    print(res)
    print(qe.execute_query(f.get_fact_query()))
