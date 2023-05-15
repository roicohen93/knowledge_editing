from fact import Fact
from testcase import TestCase
import random
from enum import Enum, auto


class TestsAxis(Enum):
    MAKING_UP = auto()
    LOGICAL_CONSTRAINTS = auto()
    SUBJECT_PARAPHRASING = auto()
    TWO_HOP = auto()
    PREVIOUS_STORAGE = auto()


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
        res = f'Fact: {str(self.fact)}\n'
        res += f'Making Up tests:\n'
        res += self.str_list_of_tests(self.making_up_tests)
        res += '\n'
        res += f'Logical Constraints:\n'
        res += self.str_list_of_tests(self.logical_constraints)
        res += '\n'
        res += f'Subject Paraphrasing tests:\n'
        res += self.str_list_of_tests(self.subject_paraphrasing_tests)
        res += '\n'
        res += f'Two-Hop tests:\n'
        res += self.str_list_of_tests(self.two_hop_tests)
        res += '\n'
        res += f'Previous Storage tests:'
        res += self.str_list_of_tests(self.prev_storage_tests)
        return res
    
    @staticmethod
    def str_list_of_tests(tests: list):
        res = ''
        for test in tests:
            res += f'{str(test)}\n'
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
