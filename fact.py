from wikidata.utils import get_label


class Fact:

    def __init__(self, subject_id, relation, target_id):
        self._subject_id = subject_id
        self._relation = relation
        self._target_id = target_id

    def get_subject_label(self):
        return get_label(self._subject_id)

    def get_target_label(self):
        return get_label(self._target_id)

    def get_relation_label(self):
        return self._relation.name.replace('_', ' ')

    def get_fact_prompt(self):
        return self._relation.phrase(get_label(self._subject_id))

    def to_dict(self):
        return {
            'subject_id': self._subject_id,
            'relation': self._relation.name,
            'target_id': self._target_id
        }
