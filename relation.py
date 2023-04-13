from enum import Enum
from wikidata.utils import subject_relation_to_targets
from utils import compute_exact_match


class Relation(Enum):

    MOTHER = ('P25', 'The mother of <subject> is', ['BROTHER', 'SISTER', 'SIBLING', 'UNCLE', 'AUNT'])
    FATHER = ('P22', 'The father of <subject> is', ['BROTHER', 'SISTER', 'SIBLING', 'UNCLE', 'AUNT'])
    BROTHER = ('P7', 'The brother of <subject> is', ['SIBLING'])
    SISTER = ('P9', 'The sister of <subject> is', ['SIBLING'])
    SIBLING = ('P3373', "<subject>'s siblings are", ['BROTHER', 'SISTER'])
    UNCLE = ('', 'The uncle of <subject> is', [])
    AUNT = ('', 'The aunt of <subject> is', [])
    CHILD = ('P40', 'The child of <subject> is', ['NUMBER_OF_CHILDREN'])
    NUMBER_OF_CHILDREN = ('P1971', 'The number of children <subject> has is', [])
    SEX_OR_GENDER = ('P21', "<subject>'s gender is", [])

    def __init__(self, relation_id, phrase, impacted_relations):
        self._relation_id = relation_id
        self._phrase = phrase
        self._impacted_relations = impacted_relations

    def id(self):
        return self._relation_id

    def phrase(self, subject):
        return self._phrase.replace('<subject>', subject)

    def evaluate(self, subject):
        return subject_relation_to_targets(subject, self._relation_id)

    def impacted_relations(self):
        return [Relation[r] for r in self._impacted_relations]

    @staticmethod
    def string_to_enum(relation_name: str):
        processed_relation_name = relation_name.replace(' ', '_')
        for relation in Relation:
            if compute_exact_match(processed_relation_name, relation.name):
                return relation
        return None
