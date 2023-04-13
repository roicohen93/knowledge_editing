import json
import random
from wikidata.utils import get_label, load_json, ent_label2id
from wikidata.relations import our_relations
from wikidata.recently_modified_facts import recently_modified_facts_given_relation
from build_benchmark_tests import making_up_axis, logical_constraints_axis, subject_aliasing_axis
from relation import Relation
from fact import Fact
from benchmark import CounterFactualExample, RecentlyAddedExample, Dataset


def construct_counterfactuals_benchmark():
    current_counterfactuals = load_json('./generations/fact_and_counterfactual_samples.json')
    dataset_list = []
    for example in current_counterfactuals:
        prev_fact = example['fact']
        prev_target_id = ent_label2id(prev_fact[1][1])
        counterfactual = example['counterfactual']
        subject, relation, target = counterfactual[0], counterfactual[1], counterfactual[2]
        subject_id, target_id = ent_label2id(subject), ent_label2id(target)
        if subject_id is None or target_id is None:
            continue
        relation_enum = Relation.string_to_enum(relation)
        if relation_enum is None:
            continue
        curr_example = CounterFactualExample(Fact(subject_id, relation_enum, target_id),
                                             Fact(subject_id, relation_enum, prev_target_id))
        dataset_list.append(curr_example)
    return Dataset(dataset_list)


if __name__ == '__main__':
    # recent_week_mother_modified = recently_modified_facts_given_relation(
    #     our_relations['mother'],
    #     k_recent_days=7,
    #     limit=10000
    # )
    #
    # example_benchmark = []
    # mother_relation_id = our_relations['mother']
    # for fact in random.sample(recent_week_mother_modified, 10):
    #     subject_id, relation_id, target_id = fact
    #     example = {
    #         'fact': (get_label(subject_id), 'mother', get_label(target_id)),
    #         'making-up axis': making_up_axis(subject_id, mother_relation_id),
    #         'logical constraints axis': logical_constraints_axis(subject_id, 'mother', target_id),
    #         'subject aliasing axis': subject_aliasing_axis(subject_id, 'mother', target_id),
    #     }
    #     example_benchmark.append(example)
    #
    # for example in example_benchmark:
    #     print(example)

    counterfactuals_dataset = construct_counterfactuals_benchmark()
    print(counterfactuals_dataset.sample(5)[0])




