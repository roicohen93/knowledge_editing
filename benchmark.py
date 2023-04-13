from fact import Fact
from testcase import TestCase
import random


class Example:

    def __init__(self,
                 fact: Fact,
                 making_up_tests: list = [],
                 logical_constraints: list = [],
                 subject_paraphrasing_tests: list = [],
                 two_hop_tests: list = [],
                 prev_storage_tests: list = []):
        self.fact = fact
        self.making_up_tests = making_up_tests
        self.logical_constraints = logical_constraints
        self.subject_paraphrasing_tests = subject_paraphrasing_tests
        self.two_hop_tests = two_hop_tests
        self.prev_storage_tests = prev_storage_tests

    def __str__(self):
        res = f'Fact: ({self.fact.get_subject_label()}, {self.fact.get_relation_label()}, {self.fact.get_target_label()})\n'
        res += f'Making Up tests: {self.making_up_tests}\n'
        res += f'Logical Constraints: {self.logical_constraints}\n'
        res += f'Subject Paraphrasing tests: {self.subject_paraphrasing_tests}\n'
        res += f'Two-Hop tests: {self.two_hop_tests}\n'
        res += f'Previous Storage tests: {self.prev_storage_tests}\n'
        return res


class CounterFactualExample(Example):

    def __init__(self,
                 fact: Fact,
                 previous_fact: Fact,
                 making_up_tests: list = [],
                 logical_constraints: list = [],
                 subject_paraphrasing_tests: list = [],
                 two_hop_tests: list = [],
                 prev_storage_tests: list = []
                 ):
        super().__init__(
            fact,
            making_up_tests,
            logical_constraints,
            subject_paraphrasing_tests,
            two_hop_tests,
            prev_storage_tests
        )
        self.previous_fact = previous_fact


class RecentlyAddedExample(Example):

    def __init__(self,
                 fact: Fact,
                 making_up_tests: list = [],
                 logical_constraints: list = [],
                 subject_paraphrasing_tests: list = [],
                 two_hop_tests: list = [],
                 prev_storage_tests: list = []
                 ):
        super().__init__(
            fact,
            making_up_tests,
            logical_constraints,
            subject_paraphrasing_tests,
            two_hop_tests,
            prev_storage_tests
        )


class Dataset:

    def __init__(self, examples: list):
        self.examples = examples

    def sample(self, k: int):
        return random.sample(self.examples, min(k, len(self.examples)))
