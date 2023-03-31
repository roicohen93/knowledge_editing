from wikidata.utils import retrieve_from_wikidata, facts_list_to_relation2targets
from collections import defaultdict


def generate_constraints(
        relation: str,
        subject: str,
        target: str,
        subject_subgraph: dict,
        target_subgraph: dict
):
    constraints = []

    if relation == 'mother' or relation == 'father':
        if relation == 'mother':
            subject_father = subject_subgraph[subject]['father']
            if subject_father:
                subject_father = subject_father[0]
                subject_father_dict = facts_list_to_relation2targets(
                    retrieve_from_wikidata(subject_father, './wikidata/wikidata_full_kg/filtered_relations'))
            else:
                subject_father = 'NA'
                subject_father_dict = defaultdict(list)
            subject_subgraph[subject_father] = subject_father_dict

            constraints.append((subject, 'father', subject_father))
            constraints.append((subject, 'parents', target + subject_father))
            constraints.append((subject, 'sibling',
                                target_subgraph[target]['child'] + subject_subgraph[subject_father]['child']))
            constraints.append((subject, 'grandparent',
                                target_subgraph[target]['mother'] + target_subgraph[target]['father'] +
                                subject_subgraph[subject_father]['mother'] + subject_subgraph[subject_father]['father']))
            constraints.append((subject, 'uncle',
                                target_subgraph[target]['sibling'] + subject_subgraph[subject_father]['sibling']))
            constraints.append((subject, 'nationality',
                                target_subgraph[target]['nationality'] + subject_subgraph[subject_father]['nationality']))

        if relation == 'father':
            subject_mother = subject_subgraph[subject]['mother']
            if subject_mother:
                subject_mother = subject_mother[0]
                subject_mother_dict = facts_list_to_relation2targets(
                    retrieve_from_wikidata(subject_mother, './wikidata/wikidata_full_kg/filtered_relations'))
            else:
                subject_mother = 'NA'
                subject_mother_dict = defaultdict(list)
            subject_subgraph[subject_mother] = subject_mother_dict

            constraints.append((subject, 'mother', subject_mother))
            constraints.append((subject, 'parents', target + subject_mother))
            constraints.append((subject, 'sibling',
                                target_subgraph[target]['child'] + subject_subgraph[subject_mother]['child']))
            constraints.append((subject, 'grandparent',
                                target_subgraph[target]['mother'] + target_subgraph[target]['father'] +
                                subject_subgraph[subject_mother]['mother'] + subject_subgraph[subject_mother]['father']))
            constraints.append((subject, 'uncle',
                                target_subgraph[target]['sibling'] + subject_subgraph[subject_mother]['sibling']))
            constraints.append((subject, 'nationality',
                                target_subgraph[target]['nationality'] + subject_subgraph[subject_mother]['nationality']))

        constraints.append((target, 'child', [subject] + target_subgraph[target]['child']))
        constraints.append((target, 'number of children', [str(len(target_subgraph[target]['child']) + 1)]))
        constraints.append((subject, 'occupation', subject_subgraph[subject]['occupation']))
        constraints.append((subject, 'ethnicity', subject_subgraph[subject]['ethnicity']))
        constraints.append((subject, 'ethnic group', subject_subgraph[subject]['ethnic group']))
        constraints.append((subject, 'place of birth', subject_subgraph[subject]['place of birth']))
        constraints.append((subject, 'date of birth', subject_subgraph[subject]['date of birth']))
        constraints.append((subject, 'award received', subject_subgraph[subject]['award received']))
        constraints.append((subject, 'child', subject_subgraph[subject]['child']))
        constraints.append((subject, 'educated at', subject_subgraph[subject]['educated at']))
        constraints.append((subject, 'notable work', subject_subgraph[subject]['notable work']))
        constraints.append((subject, 'blood type', subject_subgraph[subject]['blood type']))
        constraints.append((subject, 'eye color', subject_subgraph[subject]['eye color']))
        constraints.append((subject, 'mass', subject_subgraph[subject]['mass']))
        constraints.append((subject, 'medical condition', subject_subgraph[subject]['medical condition']))
        constraints.append((subject, 'has pet', subject_subgraph[subject]['has pet']))
        constraints.append((subject, 'handedness', subject_subgraph[subject]['handedness']))
        constraints.append((subject, 'participant in', subject_subgraph[subject]['participant in']))
        constraints.append((subject, 'influenced by', subject_subgraph[subject]['influenced by']))

    return constraints
