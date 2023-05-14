from wikidata.utils import get_label, get_aliases


class Query:

    def __init__(self, subject_id, relation, target_ids, phrase=None):
        self._subject_id = subject_id
        self._relation = relation
        self._targets_ids = target_ids if type(target_ids) == list else [target_ids]
        self._phrase = phrase

    def get_query_prompt(self):
        if self._phrase is None:
            return self._relation.phrase(get_label(self._subject_id))
        return self._phrase

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
            'answers': [{'value': get_label(target), 'aliases': get_aliases(target)} if type(target) == str and target[0] == 'Q'
                        else {'value': str(target), 'aliases': []} for target in self._targets_ids]
        }


class TwoHopQuery(Query):

    def __init__(self, subject_id, relation, target_ids, second_relation, second_hop_target_ids, phrase):
        super().__init__(subject_id, relation, target_ids, phrase)
        self._second_relation = second_relation
        self._second_hop_targets_ids = second_hop_target_ids

    def get_query_prompt(self):
        return self._phrase

    def get_answers(self):
        answers = []
        for target in self._second_hop_targets_ids:
            if type(target) is str:
                target_answer = [get_label(target)] + get_aliases(target)
            else:
                target_answer = [str(target)]
            answers.append(target_answer)
        return answers

    def to_dict(self):
        return {
            'input_prompt': self.get_query_prompt(),
            'answers': [{'value': get_label(target), 'aliases': get_aliases(target)}
                        if type(target) == str  and len(target) >= 2 and target[0] == 'Q' and target[1].isdigit()
                        else {'value': str(target), 'aliases': []} for target in self._second_hop_targets_ids]
        }
