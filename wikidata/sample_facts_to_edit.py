import json
import os
import numpy as np
import random
from utils import load_json, write_json
from config import checkable_relations
from collections import defaultdict


def top_k_most_popular_subjects(k: int):
    ent2num_of_facts = load_json('./subject2num_of_facts.json')
    num_of_ents = len(ent2num_of_facts)
    ents_list, num_of_facts_list = [None for _ in range(num_of_ents)], np.zeros(num_of_ents)

    i = 0
    for ent, num_of_facts in ent2num_of_facts.items():
        ents_list[i], num_of_facts_list[i] = ent, num_of_facts
        i += 1

    top_k_idx = np.argpartition(num_of_facts_list, -k)[-k:]
    top_k_ents = [ents_list[i] for i in top_k_idx]
    return top_k_ents


def wikidata_subset(ents: list, wikidata_dir: str):
    relevant_files = []
    for file in os.listdir(wikidata_dir):
        if file[-5:] == '.json':
            relevant_files.append(os.path.join(wikidata_dir, file))

    result_dict = defaultdict(list)
    for path in relevant_files:
        curr_part = load_json(path)
        for ent in ents:
            if ent in curr_part:
                facts = curr_part[ent]
                result_dict[ent].extend(facts)

    return result_dict


def sample_k_facts(k: int, wikidata: dict):
    checkable_ents = []
    for ent, facts in wikidata.items():
        for relation, target in facts:
            if relation in checkable_relations:
                checkable_ents.append(ent)

    sampled_ents = random.sample(checkable_ents, min(len(checkable_ents), k))
    sampled_facts = []
    for ent in sampled_ents:
        facts = wikidata[ent]
        checkable_facts = [fact for fact in facts if fact[0] in checkable_relations]
        random_fact = random.sample(checkable_facts, 1)[0]
        sampled_facts.append((ent, random_fact))

    return sampled_facts


if __name__ == '__main__':
    wikidata_dir = './wikidata_full_kg/filtered_relations'
    popular_ents = top_k_most_popular_subjects(5000)
    sub_wikidata = wikidata_subset(popular_ents, wikidata_dir)
    sampled_facts = sample_k_facts(100, sub_wikidata)
    write_json(sampled_facts, './100_sampled_facts.json')
    print(f'{len(sampled_facts)} facts were sampled')
    print(f'Examples: {random.sample(sampled_facts), 10}')


