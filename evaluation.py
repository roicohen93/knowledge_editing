from testrunner import TestRunner, TestResult, ExampleResult
from testcase import TestCase
from benchmark import Dataset, Example, TestsAxis
from fact import Fact
from collections import defaultdict
from build_benchmark import construct_recently_modified_benchmark, construct_fake_dataset_based_on_top_views_file
from queryexecutor import GPT2QueryExecutor, GPT3QueryExecutor, GPTJQueryExecutor
from modeleditor import ROMEModelEditor, InContextNaiveModelEditor
from wikidata.utils import write_json, add_to_json
from testrunner import ExampleResult


class Evaluator:

    def __init__(self, query_executor, model_editor):
        self._query_executor = query_executor
        self._model_editor = model_editor
        self._test_runner = TestRunner(query_executor, model_editor)

    def average_acc(self, example: Example, test_cases: list):
        run_res = self._test_runner.run_testcases(example, test_cases)
        fact_edit_succeeded, res_dict = run_res
        edit_succeeded = True
        if fact_edit_succeeded == ExampleResult.EDIT_FAILED or not len(test_cases):
            edit_succeeded = False
        werent_executed = len(res_dict[TestResult.NOT_EXECUTED])
        successes = len(res_dict[TestResult.PASSED])
        fails = len(res_dict[TestResult.FAILED])
        executed = (successes + fails) / (successes + fails + werent_executed)
        return successes / (successes + fails) if successes else 0.0, executed, len(test_cases), edit_succeeded

    def evaluate_making_up_axis(self, example: Example):
        return self.average_acc(example, example.making_up_tests)

    def evaluate_logical_constraints(self, example: Example):
        return self.average_acc(example, example.logical_constraints)

    def evaluate_subject_paraphrasing(self, example: Example):
        return self.average_acc(example, example.subject_paraphrasing_tests)

    def evaluate_two_hop_tests(self, example: Example):
        return self.average_acc(example, example.two_hop_tests)

    def evaluate_prev_storage_tests(self, example: Example):
        return self.average_acc(example, example.prev_storage_tests)

    def evaluate(self, example: Example):
        res = defaultdict()
        res[TestsAxis.MAKING_UP] = self.evaluate_making_up_axis(example)
        res[TestsAxis.LOGICAL_CONSTRAINTS] = self.evaluate_logical_constraints(example)
        res[TestsAxis.SUBJECT_PARAPHRASING] = self.evaluate_subject_paraphrasing(example)
        res[TestsAxis.TWO_HOP] = self.evaluate_two_hop_tests(example)
        res[TestsAxis.PREVIOUS_STORAGE] = self.evaluate_prev_storage_tests(example)
        return res


class ConditionsEvaluator(Evaluator):

    def __init__(self, query_executor):
        super(ConditionsEvaluator, self).__init__(query_executor, None)


if __name__ == '__main__':
    davinvi_query_executor = GPT3QueryExecutor(model_size='text-davinci-003')
    gpt2_query_executor = GPT2QueryExecutor('medium')
    gptj_query_executor = GPTJQueryExecutor()
    rome_editor = ROMEModelEditor('gpt2-medium')
    # evaluator = Evaluator(query_executor=davinvi_query_executor, model_editor=InContextNaiveModelEditor(davinvi_query_executor))
    evaluator = Evaluator(query_executor=gptj_query_executor, model_editor=rome_editor)
    recently_modified_facts = construct_recently_modified_benchmark(200)
    fake_facts = construct_fake_dataset_based_on_top_views_file()

    precisions_json = dict()
    num_of_examples = 1000
    succeeded_edits = 0
    average_precision = 0
    average_executed = 0
    average_size = 0
    total_checked_examples = 0
    for i, example in enumerate(fake_facts.sample(num_of_examples)):
        if i % 5 == 0:
            print(f'{i+1}/{num_of_examples}')
        try:
            davinvi_query_executor.clean_editing_prompt()
            evaluation_results = evaluator.evaluate(example)
            making_up_results = evaluation_results[TestsAxis.MAKING_UP]
            if making_up_results == -1:
                continue
            succeeded_edits += 1
            precision, executed, size = evaluator.evaluate(example)[TestsAxis.MAKING_UP]
            average_precision += precision
            average_executed += executed
            average_size += size
            precisions_json[str(example.fact)] = precision
            total_checked_examples += 1
        except :
            continue

    average_precision /= total_checked_examples
    average_executed /= total_checked_examples
    average_size /= total_checked_examples
    print(f'{(succeeded_edits / num_of_examples)*100} successful edits (out of {num_of_examples})')
    print(f'Average making-up precision is {average_precision}')
    print(f'Average portion of executed_tests is {average_executed}')
    print(f'Average total number of tests is {average_size}')

    add_to_json(d=precisions_json, path='./results_data/some_consistency_results.json')
