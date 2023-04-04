from wikidata.utils import get_label
from utils import create_test_example_given_input_targets
from relation import Relation


class Fact:

    def __init__(self, subject_id, relation, target_id):
        self._subject_id = subject_id
        self._relation = relation
        self._target_id = target_id

    def generate_conditions(self):
        pass  # TODO: Generate running conditions

    def generate_test_queries(self):
        # TODO: Generate all tests
        return self._generate_making_up_tests() + \
               self._generate_logical_constraints_tests()

    def _generate_making_up_tests(self):
        tests = []
        subject_label = get_label(self._subject_id)

        for other_relation in Relation:
            if other_relation == self._relation or other_relation in self._relation.impacted_relations():
                continue
            corresponding_targets = other_relation.evaluate(self._subject_id)
            if not corresponding_targets:
                continue
            phrase = other_relation.phrase(subject_label)
            tests.append(create_test_example_given_input_targets(phrase, corresponding_targets))

        return tests

    def _generate_logical_constraints_tests(self):
        raise NotImplementedError()  # Override in concrete classes


class MotherFact(Fact):

    def __init__(self, subject_id, target_id):
        super().__init__(subject_id, Relation.MOTHER, target_id)

    def _generate_logical_constraints_tests(self):
        constraints = []
        subject_label = get_label(self._subject_id)
        mother_label = get_label(self._target_id)

        # siblings
        mothers_children = Relation.CHILD.evaluate(self._target_id)
        father_options = Relation.FATHER.evaluate(self._subject_id)
        fathers_children = []
        for father in father_options:
            fathers_children += Relation.CHILD.evaluate(father)
        fathers_children = [child for child in fathers_children if child != self._subject_id]
        phrase = Relation.SIBLING.phrase(subject_label)
        constraints.append(create_test_example_given_input_targets(phrase, mothers_children + fathers_children))

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
        phrase = Relation.UNCLE.phrase(subject_label)
        constraints.append(create_test_example_given_input_targets(phrase, uncles))
        phrase = Relation.AUNT.phrase(subject_label)
        constraints.append(create_test_example_given_input_targets(phrase, aunts))

        # child
        phrase = Relation.CHILD.phrase(mother_label)
        constraints.append(create_test_example_given_input_targets(phrase, [self._subject_id]))  # TODO: List all children instead of only the new one?

        # number of children
        phrase = Relation.NUMBER_OF_CHILDREN.phrase(mother_label)
        constraints.append(create_test_example_given_input_targets(phrase, [len(mothers_children) + 1]))

        return constraints


if __name__ == '__main__':
    f = MotherFact('Q26876', 'Q13133')  # Taylor Swift's mother is now Michelle Obama
    a = f.generate_test_queries()
    import json
    print(json.dumps(a, indent=2))
