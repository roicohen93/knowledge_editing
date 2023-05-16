import json
import random
from wikidata.utils import get_label, load_json, ent_label2id, subject_relation_to_targets, ent_to_relation_ids
from wikidata.relations import our_relations
from wikidata.recently_modified_facts import recently_modified_facts_given_relation
from build_benchmark_tests import \
    making_up_axis, \
    logical_constraints_axis, \
    subject_aliasing_axis, \
    two_hop_axis, \
    temporal_axis
from relation import Relation
from fact import Fact
from benchmark import CounterFactualExample, RecentlyAddedExample, Dataset
from queryexecutor import QueryExecutor


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


def construct_recently_modified_benchmark(size: int = None):
    current_data = load_json('./generations/uniformly_from_recent_days_recently_modified_dataset.json')
    if size is not None:
        current_data = random.sample(current_data, min(size, len(current_data)))
    dataset_list = []
    i = 0
    for subject_id, relation_id, target_id in current_data:
        relation_enum = Relation.id_to_enum(relation_id)
        if relation_enum is None:
            continue
        try:
            dataset_list.append(build_recently_modified_dataset_example(subject_id, relation_enum, target_id))
        except:
            continue
        i += 1
        if i % 100 == 0:
            print(f'Built {i}/{len(current_data)}')
    return Dataset(dataset_list)


def build_recently_modified_dataset_example(subject_id: str, relation: Relation, target_id: str):
    fact = Fact(subject_id, relation, target_id)
    making_up_tests = making_up_axis(subject_id, relation)
    logical_constraints = logical_constraints_axis(subject_id, relation, target_id)
    subject_aliasing_tests = subject_aliasing_axis(subject_id, relation, target_id)
    two_hop_tests = two_hop_axis(subject_id, relation, target_id)
    curr_example = RecentlyAddedExample(
        fact=fact,
        making_up_tests=making_up_tests,
        logical_constraints=logical_constraints,
        subject_paraphrasing_tests=subject_aliasing_tests,
        two_hop_tests=two_hop_tests
    )
    return curr_example


def construct_fake_edits_benchmark(facts:list):
    dataset_list = []
    for subject_id, relation, target_id in facts:
        relation2optional_targets = load_json('./wikidata/relation2optional_targets.json')
        relation_formal_name = relation.formal_name()
        if relation_formal_name not in relation2optional_targets:
            continue
        optional_targets = relation2optional_targets[relation.formal_name()]
        random_target_id = ent_label2id(random.sample(optional_targets, 1)[0])
        if random_target_id is None:
            continue
        dataset_list.append(build_fake_dataset_example(subject_id, relation, target_id, random_target_id))
    return Dataset(dataset_list)


def build_fake_dataset_example(subject_id: str, relation: Relation, target_id: str, previous_target_id: str):
    fact = Fact(subject_id, relation, target_id)
    previous_fact = Fact(subject_id, relation, previous_target_id)
    making_up_tests = making_up_axis(subject_id, relation)
    logical_constraints = logical_constraints_axis(subject_id, relation, target_id)
    subject_aliasing_tests = subject_aliasing_axis(subject_id, relation, target_id)
    two_hop_tests = two_hop_axis(subject_id, relation, target_id)
    temporal_tests = temporal_axis(subject_id, relation, previous_target_id)
    curr_example = CounterFactualExample(
        fact=fact,
        previous_fact=previous_fact,
        making_up_tests=making_up_tests,
        logical_constraints=logical_constraints,
        subject_paraphrasing_tests=subject_aliasing_tests,
        two_hop_tests=two_hop_tests,
        prev_storage_tests=temporal_tests,
    )
    return curr_example


def filter_facts_based_on_conditions_passed(facts: list, query_executor: QueryExecutor):
    filtered_facts = []
    for subject_id, relation_enum, target_id, prev_target_id in facts:
        example = build_fake_dataset_example(subject_id, relation_enum, target_id, prev_target_id)


def all_relevant_facts_given_list_of_subjects(subjects: list):
    facts = []
    for subject_id in subjects:
        relevant_relation_ids = ent_to_relation_ids(subject_id)
        for relation_id in relevant_relation_ids:
            relation_enum = Relation.id_to_enum(relation_id)
            if relation_enum is None:
                continue
            targets = subject_relation_to_targets(subject_id, relation_id)
            for target_id in targets:
                facts.append((subject_id, relation_enum, target_id))
    return facts


def sample_relevant_facts_given_list_of_subjects(subjects: list, number_of_facts_each: int):
    facts = []
    for i, subject_id in enumerate(subjects):
        if (i+1) % 100 == 0:
            print(f'{i+1}/{len(subjects)}')
        relevant_relation_ids = ent_to_relation_ids(subject_id)
        sampled_relations_ids = random.sample(relevant_relation_ids, min(number_of_facts_each, len(relevant_relation_ids)))
        for relation_id in sampled_relations_ids:
            relation_enum = Relation.id_to_enum(relation_id)
            if relation_enum is None:
                continue
            targets = subject_relation_to_targets(subject_id, relation_id)
            if targets:
                random_target = random.sample(targets, 1)[0]
                facts.append((subject_id, relation_enum, random_target))
    return facts


def construct_fake_dataset_based_on_top_views_file(limit: int = None, limit_num_of_facts: int = None):
    subjects_json = load_json('./wikidata/top_entities_by_views_monthly.json')
    subject_list = []
    for month, subjects in subjects_json.items():
        subject_list.extend(subjects)
    subject_ids = [subject['id'] for subject in subject_list]
    if limit is not None:
        subject_ids = random.sample(subject_ids, min(limit, len(subject_ids)))
    print('extracting facts..')
    if limit_num_of_facts is None:
        all_relevant_facts = all_relevant_facts_given_list_of_subjects(subject_ids)
    else:
        all_relevant_facts = sample_relevant_facts_given_list_of_subjects(subject_ids, limit_num_of_facts)
    print('building dataset..')
    dataset = construct_fake_edits_benchmark(all_relevant_facts)
    return dataset
        

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

    # counterfactuals_dataset = construct_counterfactuaals_benchmark()
    # print(counterfactuals_dataset.sample(5)[0])

    recently_modified_benchmark = construct_recently_modified_benchmark()
    recently_modified_benchmark.examples = random.sample(recently_modified_benchmark.examples, 20000)
    recently_modified_benchmark.to_file('./benchmark/recently_modified.json')

    # for example in recently_modified_facts.sample(5):
    #     if example.fact._relation == Relation.MOTHER or example.fact._relation == Relation.FATHER:
    #         print(example)
    
    # subjects_json = load_json('./wikidata/top_entities_by_views.json')
    # subject_ids = [subject['id'] for subject in subjects_json][:5]
    # print('extracting facts..')
    # all_relevant_facts = all_relevant_facts_given_list_of_subjects(subject_ids)
    # print('building dataset..')
    # dataset = construct_fake_edits_benchmark(all_relevant_facts)
    # for example in dataset.sample(5):
    #     print(example)

    # top_views_benchmark = construct_fake_dataset_based_on_top_views_file(limit=5000, limit_num_of_facts=3)
    # top_views_benchmark.to_file('./benchmark/top_views.json')







