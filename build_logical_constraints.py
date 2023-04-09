import json
import os
from wikidata.utils import load_json, write_json, get_label, get_aliases, subject_relation_to_targets
from wikidata.relations import our_relations, relation2phrase
from utils import create_test_example_given_input_targets
from relation import Relation
from query import Query
from testcase import TestCase


class RelationalConstraints:

    def __init__(self, subject_id, edits={}):
        self.subject_id = subject_id
        self.edits = edits
        self.conditions = []

    def _targets(self, relation: Relation):
        return self.edits[relation] if relation in self.edits else subject_relation_to_targets(
            self.subject_id, relation)

    @staticmethod
    def _targets_of(self, subject_ids: list, relation: Relation):
        targets = []
        for subject_id in subject_ids:
            targets += subject_relation_to_targets(subject_id, relation)
            self.conditions.append(Query(subject_id, relation, targets))
        return targets

    def sibling(self):
        self.conditions = []
        mothers = self._targets(Relation.MOTHER)
        fathers = self._targets(Relation.FATHER)
        mother_children = self._targets_of(mothers, Relation.CHILD)
        father_children = self._targets_of(fathers, Relation.CHILD)
        return TestCase(
            test_query=Query(self.subject_id, Relation.SIBLING, mother_children + father_children),
            condition_queries=self.conditions
        )


def generate_constraints(subject_id: str, relation: Relation, new_target_id: str):
    constraints = []
    subject_label = get_label(subject_id)

    if relation == Relation.MOTHER:
        mother_label = get_label(new_target_id)

        # siblings
        phrase = relation2phrase['sibling'].replace('<subject>', subject_label)
        mothers_children = subject_relation_to_targets(new_target_id, Relation.CHILD.id())
        father_options = subject_relation_to_targets(subject_id, Relation.FATHER.id())
        father_children = []
        for father in father_options:
            father_children += subject_relation_to_targets(father, Relation.CHILD.id())
        constraints.append(create_test_example_given_input_targets(phrase, mothers_children + father_children))

        # uncle
        phrase = relation2phrase['uncle'].replace('<subject>', subject_label)
        new_uncles = []
        mother_siblings = subject_relation_to_targets(new_target_id, our_relations['sibling'])
        father_siblings = []
        for father in father_options:
            father_siblings += subject_relation_to_targets(father, our_relations['sibling'])
        for optional_uncle in mother_siblings + father_siblings:
            if get_label(subject_relation_to_targets(optional_uncle, our_relations['sex or gender'])[0]) == 'male':
                new_uncles.append(optional_uncle)
        constraints.append(create_test_example_given_input_targets(phrase, new_uncles))

        # aunt
        phrase = relation2phrase['aunt'].replace('<subject>', subject_label)
        new_aunts = []
        for optional_aunt in mother_siblings + father_siblings:
            if get_label(subject_relation_to_targets(optional_aunt, our_relations['sex or gender'])[0]) == 'female':
                new_aunts.append(optional_aunt)
        constraints.append(create_test_example_given_input_targets(phrase, new_aunts))

        # child
        phrase = relation2phrase['child'].replace('<subject>', mother_label)
        constraints.append(create_test_example_given_input_targets(phrase, [subject_id]))

        # number of children
        phrase = relation2phrase['number of children'].replace('<subject>', mother_label)
        constraints.append(create_test_example_given_input_targets(phrase, [len(mothers_children) + 1]))

    return constraints



