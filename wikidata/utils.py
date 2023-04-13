import json
import os
from collections import defaultdict
from qwikidata.linked_data_interface import get_entity_dict_from_api
from qwikidata.entity import WikidataItem


def load_json(path: str):
    with open(path, 'r+', encoding='utf-8') as f:
        result = json.load(f)
    return result


def write_json(d: dict, path: str):
    with open(path, 'w+', encoding='utf-8') as f:
        json.dump(d, f)


def retrieve_from_wikidata(ent: str, wikidata_dir: str = './wikidata_full_kg/filtered_relations'):
    if not ent:
        return None
    relevant_files = []
    for file in os.listdir(wikidata_dir):
        if file[-5:] == '.json':
            relevant_files.append(os.path.join(wikidata_dir, file))

    for path in relevant_files:
        curr_part = load_json(path)
        if ent in curr_part:
            return curr_part[ent]
    return None


def facts_list_to_relation2targets(facts: list):
    relation2targets = defaultdict(list)
    for relation, target in facts:
        relation2targets[relation].append(target)
    return relation2targets


def wikidata_item_given_id(ent_id: str):
    return WikidataItem(get_entity_dict_from_api(ent_id))


def get_label(ent_id: str):
    return wikidata_item_given_id(ent_id).get_label()


def get_aliases(ent_id: str):
    return wikidata_item_given_id(ent_id).get_aliases()


def get_description(ent_id: str):
    return wikidata_item_given_id(ent_id).get_description()


def get_targets_given_item_and_relation(item: WikidataItem, relation_id: str):
    related_claims = item.get_truthy_claim_groups()
    if relation_id not in related_claims:
        return []
    curr_relation_claims = related_claims[relation_id]
    target_ids = [claim.mainsnak.datavalue.value["id"] for claim in curr_relation_claims]
    return target_ids


def subject_relation_to_targets(subject_id: str, relation):
    relation_id = relation.id()
    subject_item = wikidata_item_given_id(subject_id)
    return get_targets_given_item_and_relation(subject_item, relation_id)


ent_label2id_dict = load_json('./wikidata/ent_label2id.json')


def ent_label2id(label: str):
    if label not in ent_label2id_dict:
        return None
    return ent_label2id_dict[label]

