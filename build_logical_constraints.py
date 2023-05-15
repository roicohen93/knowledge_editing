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

    def _targets_of(self, subject_ids: list, relation: Relation):
        targets = []
        for subject_id in subject_ids:
            targets += subject_relation_to_targets(subject_id, relation)
            self.conditions.append(Query(subject_id, relation, targets))
        return targets

    def empty_conditions(self):
        self.conditions = []

    def sibling(self):
        self.empty_conditions()
        mothers = self._targets(Relation.MOTHER)
        fathers = self._targets(Relation.FATHER)
        mother_children = self._targets_of(mothers, Relation.CHILD)
        father_children = self._targets_of(fathers, Relation.CHILD)
        return TestCase(
            test_query=Query(self.subject_id, Relation.SIBLING, mother_children + father_children),
            condition_queries=self.conditions
        )

    def mothers_child(self):
        mother = self._targets(Relation.MOTHER)[0]
        return TestCase(
            test_query=Query(mother, Relation.CHILD, [self.subject_id]),
            condition_queries=[]
        )

    def fathers_child(self):
        father = self._targets(Relation.FATHER)[0]
        return TestCase(
            test_query=Query(father, Relation.CHILD, [self.subject_id]),
            condition_queries=[]
        )

    def sibling_of_brother(self):
        brother = self._targets(Relation.BROTHER)[0]
        return TestCase(
            test_query=Query(brother, Relation.SIBLING, [self.subject_id]),
            condition_queries=[]
        )

    def mothers_number_of_children(self):
        self.empty_conditions()
        mother = self._targets(Relation.MOTHER)[0]
        num_children = len(self._targets_of([mother], Relation.CHILD))
        return TestCase(
            test_query=Query(mother, Relation.NUMBER_OF_CHILDREN, num_children + 1),
            condition_queries=self.conditions
        )

    def fathers_number_of_children(self):
        self.empty_conditions()
        father = self._targets(Relation.FATHER)[0]
        num_children = len(self._targets_of([father], Relation.CHILD))
        return TestCase(
            test_query=Query(father, Relation.NUMBER_OF_CHILDREN, num_children + 1),
            condition_queries=self.conditions
        )

    def uncle(self):
        self.empty_conditions()
        mothers = self._targets(Relation.MOTHER)
        fathers = self._targets(Relation.FATHER)
        mother_siblings = self._targets_of(mothers, Relation.SIBLING)
        male_mother_siblings = [sibling for sibling in mother_siblings
                                if get_label(subject_relation_to_targets(sibling, Relation.SEX_OR_GENDER)[0]) == 'male']
        father_siblings = self._targets_of(fathers, Relation.SIBLING)
        male_father_siblings = [sibling for sibling in father_siblings
                                if get_label(subject_relation_to_targets(sibling, Relation.SEX_OR_GENDER)[0]) == 'male']
        return TestCase(
            test_query=Query(self.subject_id, Relation.UNCLE, male_mother_siblings + male_father_siblings),
            condition_queries=self.conditions
        )

    def aunt(self):
        self.empty_conditions()
        mothers = self._targets(Relation.MOTHER)
        fathers = self._targets(Relation.FATHER)
        mother_siblings = self._targets_of(mothers, Relation.SIBLING)
        female_mother_siblings = [sibling for sibling in mother_siblings
                                if get_label(subject_relation_to_targets(sibling, Relation.SEX_OR_GENDER)[0]) == 'female']
        father_siblings = self._targets_of(fathers, Relation.SIBLING)
        female_father_siblings = [sibling for sibling in father_siblings
                                if get_label(subject_relation_to_targets(sibling, Relation.SEX_OR_GENDER)[0]) == 'female']
        return TestCase(
            test_query=Query(self.subject_id, Relation.AUNT, female_mother_siblings + female_father_siblings),
            condition_queries=self.conditions
        )


def generate_constraints(subject_id: str, relation: Relation, new_target_id: str):
    tests = []

    if relation == Relation.MOTHER:
        constraints = RelationalConstraints(subject_id, {Relation.MOTHER: [new_target_id]})
        tests.append(constraints.sibling())
        tests.append(constraints.uncle())
        tests.append(constraints.aunt())
        tests.append(constraints.mothers_child())
        tests.append(constraints.mothers_number_of_children())

    if relation == Relation.FATHER:
        constraints = RelationalConstraints(subject_id, {Relation.FATHER: [new_target_id]})
        tests.append(constraints.sibling())
        tests.append(constraints.uncle())
        tests.append(constraints.aunt())
        tests.append(constraints.fathers_child())
        tests.append(constraints.fathers_number_of_children())

    if relation == Relation.BROTHER:
        constraints = RelationalConstraints(subject_id, {Relation.BROTHER: [new_target_id]})
        # mother or father child
        tests.append(constraints.sibling_of_brother())

    return tests



