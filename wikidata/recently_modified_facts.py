import sys
from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)
from qwikidata.json_dump import WikidataJsonDump
from qwikidata.utils import dump_entities_to_json
from qwikidata.entity import WikidataItem, WikidataLexeme, WikidataProperty
from qwikidata.linked_data_interface import get_entity_dict_from_api


def extract_ent_id_from_url(url: str):
    pointer = len(url) - 1
    while url[pointer] != '/':
        pointer -= 1
    return url[pointer+1:]


def recently_modified_facts_given_relation(relation_id: str, k_recent_days: int = 7, limit: int = 100):
    sparql_query = f"""
    SELECT DISTINCT ?item ?target ?date_modified
    WHERE
    {{
      ?item wdt:{relation_id} ?target ;
              schema:dateModified ?date_modified .
        BIND (now() - ?date_modified as ?date_range)
        FILTER (?date_range < {k_recent_days + 1})
      
        SERVICE wikibase:label {{
          bd:serviceParam wikibase:language "en" .
         }}
    }}
    LIMIT {limit}
    """

    res = return_sparql_query_results(sparql_query)

    resulted_facts = []
    for returned_fact in res['results']['bindings']:
        subject, target = returned_fact['item'], returned_fact['target']

        # handling subject
        if subject['type'] == 'uri':
            subject = extract_ent_id_from_url(subject['value'])
        elif subject['type'] == 'literal':
            subject = subject['value']

        # handling target
        if target['type'] == 'uri':
            target = extract_ent_id_from_url(target['value'])
        elif target['type'] == 'literal':
            target = target['value']

        resulted_facts.append((subject, relation_id, target))

    return resulted_facts
