from wikidata.utils import get_label, get_aliases


class Query:

    def __init__(self, subject_id, relation, target_ids):
        self._subject_id = subject_id
        self._relation = relation
        self._targets_ids = target_ids if type(target_ids) == list else [target_ids]

    def get_query_prompt(self):
        return self._relation.phrase(get_label(self._subject_id))

    def get_answers(self):
        answers = []
        for target in self._targets_ids:
            if type(target) is str:
                target_answer = [get_label(target)] + get_aliases(target)
            else:
                target_answer = [str(target)]
            answers.append(target_answer)
        return answers

    def to_dict(self):
        return {
            'input_prompt': self.get_query_prompt(),
            'answers': [{'value': get_label(target), 'aliases': get_aliases(target)} if type(target) == str
                        else {'value': str(target), 'aliases': []} for target in self._targets_ids]
        }
