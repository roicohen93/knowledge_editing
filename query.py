from wikidata.utils import get_label, get_aliases


class Query:

    def __init__(self, subject_id, relation, target_ids):
        self._subject_id = subject_id
        self._relation = relation
        self._targets_ids = target_ids

    def to_dict(self):
        return {
            'input_prompt': self._relation.phrase(get_label(self._subject_id)),
            'answers': [{'value': get_label(target), 'aliases': get_aliases(target)} if type(target) == str
                        else {'value': str(target), 'aliases': []} for target in self._targets_ids]
        }
