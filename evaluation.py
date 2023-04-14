from testrunner import TestRunner, TestResult
from testcase import TestCase
from benchmark import Dataset, Example, TestsAxis
from fact import Fact
from collections import defaultdict


class Evaluator:

    def __init__(self, query_executor, model_editor):
        self._query_executor = query_executor
        self._model_editor = model_editor
        self._test_runner = TestRunner(query_executor, model_editor)

    def average_acc(self, fact: Fact, test_cases: list):
        res_dict = self._test_runner.run_testcases(fact, test_cases)
        didnt_execute = len(res_dict[TestResult.NOT_EXECUTED])
        successes = len(res_dict[TestResult.PASSED])
        fails = len(res_dict[TestResult.FAILED])
        return successes / (successes + fails) if successes else 0.0, didnt_execute

    def evaluate_making_up_axis(self, example: Example):
        return self.average_acc(example.fact, example.making_up_tests)

    def evaluate_logical_constraints(self, example: Example):
        return self.average_acc(example.fact, example.logical_constraints)

    def evaluate_subject_paraphrasing(self, example: Example):
        return self.average_acc(example.fact, example.subject_paraphrasing_tests)

    def evaluate_two_hop_tests(self, example: Example):
        return self.average_acc(example.fact, example.two_hop_tests)

    def evaluate_prev_storage_tests(self, example: Example):
        return self.average_acc(example.fact, example.prev_storage_test)

    def evaluate(self, example: Example):
        res = defaultdict()
        res[TestsAxis.MAKING_UP] = self.evaluate_making_up_axis(example)
        res[TestsAxis.LOGICAL_CONSTRAINTS] = self.evaluate_logical_constraints(example)
        res[TestsAxis.SUBJECT_PARAPHRASING] = self.evaluate_subject_paraphrasing(example)
        res[TestsAxis.TWO_HOP] = self.evaluate_two_hop_tests(example)
        res[TestsAxis.PREVIOUS_STORAGE] = self.evaluate_prev_storage_tests(example)
        return res
