from wikidata.relations import our_relations, relation2impacted_relations, relation2phrase
from wikidata.utils import subject_relation_to_targets, get_label, get_aliases, get_description
from build_logical_constraints import generate_constraints
from utils import create_test_example_given_input_targets


def making_up_axis(subject_id, relation):
    tests = []

    if relation not in our_relations:
        return tests

    subject_label = get_label(subject_id)
    impacted_relations = relation2impacted_relations[relation]
    for other_relation in our_relations:
        if other_relation == relation or other_relation in impacted_relations:
            continue
        corresponding_targets = subject_relation_to_targets(subject_id, our_relations[other_relation])
        if not corresponding_targets:
            continue
        phrase = relation2phrase[other_relation].replace('<subject>', subject_label)
        test = {
            'input_prompt': phrase,
            'answers': [{'value': get_label(target), 'aliases': get_aliases(target)} for target in corresponding_targets]
        }
        tests.append(test)

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


