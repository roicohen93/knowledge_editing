from testrunner import TestRunner, TestResult, ExampleResult
from testcase import TestCase
from benchmark import Dataset, Example, TestsAxis
from fact import Fact
from collections import defaultdict
from build_benchmark import construct_recently_modified_benchmark, construct_fake_dataset_based_on_top_views_file
from queryexecutor import GPT2QueryExecutor, GPT3QueryExecutor, GPTJQueryExecutor, GPTNeoXQueryExecutor, LlamaQueryExecutor
from modeleditor import ROMEModelEditor, InContextNaiveModelEditor
from wikidata.utils import write_json, add_to_json
from testrunner import ExampleResult
from collections import defaultdict


class Evaluator:

    def __init__(self, query_executor, model_editor):
        self._query_executor = query_executor
        self._model_editor = model_editor
        self._test_runner = TestRunner(query_executor, model_editor)

    def average_acc(self, example: Example, test_cases: list, skip_edit: bool = False, skip_restore: bool = False):
        if not len(test_cases) and skip_edit:
            return 0.0, 0.0, 0.0, False

        run_res = self._test_runner.run_testcases(example, test_cases, skip_edit=skip_edit, skip_restore=skip_restore)
        fact_edit_succeeded, res_dict = run_res
        edit_succeeded = True
        if fact_edit_succeeded == ExampleResult.EDIT_FAILED:
            edit_succeeded = False

        if not len(test_cases):
            return 0.0, 0.0, 0.0, edit_succeeded

        werent_executed = len(res_dict[TestResult.NOT_EXECUTED])
        successes = len(res_dict[TestResult.PASSED])
        fails = len(res_dict[TestResult.FAILED])
        executed = (successes + fails) / (successes + fails + werent_executed)
        return successes / (successes + fails) if successes else 0.0, executed, len(test_cases), edit_succeeded

    def evaluate_making_up_axis(self, example: Example):
        return self.average_acc(example, example.making_up_tests, skip_restore=True)

    def evaluate_logical_constraints(self, example: Example):
        return self.average_acc(example, example.logical_constraints, skip_edit=True, skip_restore=True)

    def evaluate_subject_paraphrasing(self, example: Example):
        return self.average_acc(example, example.subject_paraphrasing_tests, skip_edit=True, skip_restore=True)

    def evaluate_two_hop_tests(self, example: Example):
        return self.average_acc(example, example.two_hop_tests, skip_edit=True, skip_restore=True)

    def evaluate_forward_two_hop_tests(self, example: Example):
        return self.average_acc(example, example.forward_two_hop_tests, skip_edit=True, skip_restore=True)

    def evaluate_prev_storage_tests(self, example: Example):
        return self.average_acc(example, example.prev_storage_tests, skip_edit=True, skip_restore=False)

    def evaluate(self, example: Example):
        res = defaultdict()
        res[TestsAxis.MAKING_UP] = self.evaluate_making_up_axis(example)
        res[TestsAxis.LOGICAL_CONSTRAINTS] = self.evaluate_logical_constraints(example)
        res[TestsAxis.SUBJECT_PARAPHRASING] = self.evaluate_subject_paraphrasing(example)
        res[TestsAxis.TWO_HOP] = self.evaluate_two_hop_tests(example)
        res[TestsAxis.FORWARD_TWO_HOP] = self.evaluate_forward_two_hop_tests(example)
        res[TestsAxis.PREVIOUS_STORAGE] = self.evaluate_prev_storage_tests(example)
        return res


class ConditionsEvaluator(Evaluator):

    def __init__(self, query_executor):
        super(ConditionsEvaluator, self).__init__(query_executor, None)


if __name__ == '__main__':
    model = 'gpt-j'
    editor = 'rome'
    dataset_path = './benchmark/filtered/gpt-j_1000.json'

    davinvci_query_executor = GPT3QueryExecutor(model_size='text-davinci-003')
    if model == 'gpt2-medium':
        query_executor = GPT2QueryExecutor('medium')
    if model == 'gpt2-large':
        query_executor = GPT2QueryExecutor('large')
    if model == 'gpt2-xl':
        query_executor = GPT2QueryExecutor('xl')
    if model == 'gpt-j':
        query_executor =GPTJQueryExecutor()
    if model == 'gpt-neo':
        query_executor = GPTNeoXQueryExecutor()
    if model == 'llama':
        query_executor = LlamaQueryExecutor()

    if editor == 'rome':
        model_editor = ROMEModelEditor(query_executor)

    # evaluator = Evaluator(query_executor=davinvi_query_executor, model_editor=InContextNaiveModelEditor(davinvi_query_executor))
    evaluator = Evaluator(query_executor=query_executor, model_editor=model_editor)
    dataset = Dataset.from_file(dataset_path)

    precisions_json = dict()
    num_of_examples = 200

    examples_for_eval = dataset.sample(num_of_examples)
    eval_size = len(examples_for_eval)

    succeeded_edits = defaultdict(lambda: 0)
    average_precision = defaultdict(lambda: 0)
    average_executed = defaultdict(lambda: 0)
    average_size = defaultdict(lambda: 0)
    total_checked_examples = defaultdict(lambda: 0)
    executed_portion_dict = defaultdict(lambda: 0)

    for i, example in enumerate(examples_for_eval):
        if (i+1) % 10 == 0:
            print(f'{i+1}/{eval_size}')

        davinvci_query_executor.clean_editing_prompt()
        evaluation_results = evaluator.evaluate(example)

        for axis, results in evaluation_results.items():
            precision, executed, size, edit_succeeded = results
            if executed == 0.0:
                continue
            if edit_succeeded:
                succeeded_edits[axis] += 1
            average_precision[axis] += precision
            average_executed[axis] += executed
            average_size[axis] += size
            precisions_json[str(example.fact)] = precision
            total_checked_examples[axis] += 1

        for axis in TestsAxis:
            if axis in evaluation_results:
                executed_portion_dict[axis] += evaluation_results[axis][1]

    for axis in TestsAxis:
        print(f'Results of axis {axis}:')

        if total_checked_examples[axis] == 0:
            print(f'No checked tests for this axis')
            continue

        average_precision[axis] /= total_checked_examples[axis]
        average_executed[axis] /= total_checked_examples[axis]
        average_size[axis] /= total_checked_examples[axis]

        print(f'{(succeeded_edits[axis]  / eval_size)*100} successful edits (out of {eval_size})')
        print(f'Average making-up precision is {average_precision[axis] }')
        print(f'Average portion of executed_tests is {average_executed[axis] }')
        print(f'Average total number of tests is {average_size[axis] }')

    add_to_json(d=precisions_json, path=f'./results_data/{model}_{editor}.json')
