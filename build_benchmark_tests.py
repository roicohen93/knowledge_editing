from wikidata.relations import our_relations, relation2impacted_relations, relation2phrase
from wikidata.utils import subject_relation_to_targets, get_label, get_aliases, get_description
from build_logical_constraints import generate_constraints
from utils import create_test_example_given_input_targets
from relation import Relation
from query import Query
from testcase import TestCase


def making_up_axis(subject_id: str, relation: Relation):
    tests = []

    if relation not in Relation:
        return tests

    impacted_relations = relation.impacted_relations()
    for other_relation in Relation:
        if other_relation == relation or other_relation in impacted_relations:
            continue
        corresponding_targets = subject_relation_to_targets(subject_id, other_relation)
        if not corresponding_targets:
            continue
        test_query = Query(subject_id, other_relation, corresponding_targets)
        condition_queries = [test_query]
        tests.append(TestCase(test_query=test_query, condition_queries=condition_queries))

    return tests


def logical_constraints_axis(subject_id, relation, target_id):
    return generate_constraints(subject_id, relation, target_id)


def subject_aliasing_axis(subject_id, relation, target_id):
    tests = []
    subject_description = get_description(subject_id)
    phrase = relation2phrase[relation].replace('<subject>', subject_description)
    tests.append(create_test_example_given_input_targets(phrase, [target_id]))
    return tests
    

# for test in subject_aliasing_axis('Q42', 'occupation', 'Q36834'):
#     print(test)


