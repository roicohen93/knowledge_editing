from fact import Fact
from testcase import TestCase


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
