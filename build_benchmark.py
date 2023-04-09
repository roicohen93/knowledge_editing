import json
import random
from wikidata.utils import get_label
from wikidata.relations import our_relations
from wikidata.recently_modified_facts import recently_modified_facts_given_relation
from build_benchmark_tests import making_up_axis, logical_constraints_axis, subject_aliasing_axis


if __name__ == '__main__':
    recent_week_mother_modified = recently_modified_facts_given_relation(
        our_relations['mother'],
        k_recent_days=7,
        limit=10000
    )

    example_benchmark = []
    mother_relation_id = our_relations['mother']
    for fact in random.sample(recent_week_mother_modified, 10):
        subject_id, relation_id, target_id = fact
        example = {
            'fact': (get_label(subject_id), 'mother', get_label(target_id)),
            'making-up axis': making_up_axis(subject_id, mother_relation_id),
            'logical constraints axis': logical_constraints_axis(subject_id, 'mother', target_id),
            'subject aliasing axis': subject_aliasing_axis(subject_id, 'mother', target_id),
        }
        example_benchmark.append(example)

    for example in example_benchmark:
        print(example)