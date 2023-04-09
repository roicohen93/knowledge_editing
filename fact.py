from wikidata.utils import get_label
from relation import Relation
from query import Query
from testcase import TestCase


class Fact:

    def __init__(self, subject_id, relation, target_id):
        self._subject_id = subject_id
        self._relation = relation
        self._target_id = target_id

    def get_subject_label(self):
        return get_label(self._subject_id)

    def get_target_label(self):
        return get_label(self._target_id)

    def get_fact_prompt(self):
        return self._relation.phrase(get_label(self._subject_id))

    def to_dict(self):
        return {
            'subject_id': self._subject_id,
            'relation': self._relation.name,
            'target_id': self._target_id
        }

    def generate_tests(self):
        # TODO: Generate all tests
        return self._generate_making_up_tests() + \
               self._generate_logical_constraints_tests()

    def _generate_making_up_tests(self):
        tests = []
        for other_relation in Relation:
            if other_relation == self._relation or other_relation in self._relation.impacted_relations():
                continue
            corresponding_targets = other_relation.evaluate(self._subject_id)
            if not corresponding_targets:
                continue
            query = Query(self._subject_id, other_relation, corresponding_targets)
            tests.append(TestCase(self, query, [query]))  # Making up tests check that the query answer doesn't change
        return tests

    def _generate_logical_constraints_tests(self):
        raise NotImplementedError()  # Override in concrete classes


class MotherFact(Fact):

    def __init__(self, subject_id, target_id):
        super().__init__(subject_id, Relation.MOTHER, target_id)

    def _generate_logical_constraints_tests(self):
        tests = []

        # siblings
        mothers_children = Relation.CHILD.evaluate(self._target_id)
        father_options = Relation.FATHER.evaluate(self._subject_id)
        fathers_children = []
        for father in father_options:
            fathers_children += Relation.CHILD.evaluate(father)
        fathers_children = [child for child in fathers_children if child != self._subject_id]
        query = Query(self._subject_id, Relation.SIBLING, mothers_children + fathers_children)
        conditions = []  # TODO: Add conditions
        tests.append(TestCase(self, query, conditions))

        # uncles and aunts
        mothers_siblings = Relation.SIBLING.evaluate(self._target_id)
        father_siblings = []
        for father in father_options:
            father_siblings += Relation.SIBLING.evaluate(father)
        uncles = []
        aunts = []
        for parent_sibling in mothers_siblings + father_siblings:
            gender = get_label(Relation.SEX_OR_GENDER.evaluate(parent_sibling)[0])
            if gender == 'male':
                uncles.append(parent_sibling)
            elif gender == 'female':
                aunts.append(parent_sibling)
        query = Query(self._subject_id, Relation.UNCLE, uncles)
        conditions = []  # TODO: Add conditions
        tests.append(TestCase(self, query, conditions))
        query = Query(self._subject_id, Relation.AUNT, aunts)
        conditions = []  # TODO: Add conditions
        tests.append(TestCase(self, query, conditions))

        # child
        query = Query(self._target_id, Relation.CHILD, [self._subject_id])  # TODO: List all children instead of only the new one?
        conditions = []  # TODO: Add conditions
        tests.append(TestCase(self, query, conditions))

        # number of children
        query = Query(self._target_id, Relation.NUMBER_OF_CHILDREN, [len(mothers_children) + 1])
        conditions = []  # TODO: Add conditions
        tests.append(TestCase(self, query, conditions))

        return tests


if __name__ == '__main__':
    f = MotherFact('Q26876', 'Q13133')  # Taylor Swift's mother is now Michelle Obama
    a = [test.to_dict() for test in f.generate_tests()]
    import json
    print(json.dumps(a, indent=2))