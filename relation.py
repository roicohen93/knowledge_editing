from enum import Enum
from wikidata.utils import subject_relation_to_targets
from utils import compute_exact_match


class Relation(Enum):

    MOTHER = ('P25', 'The mother of <subject> is', ['BROTHER', 'SISTER', 'SIBLING', 'UNCLE', 'AUNT'], True)
    FATHER = ('P22', 'The father of <subject> is', ['BROTHER', 'SISTER', 'SIBLING', 'UNCLE', 'AUNT'], True)
    BROTHER = ('P7', 'The brother of <subject> is', ['SIBLING'], False)
    SISTER = ('P9', 'The sister of <subject> is', ['SIBLING'], False)
    SIBLING = ('P3373', "<subject>'s siblings are", ['BROTHER', 'SISTER'], False)
    SPOUSE = ('P26', "<subject>'s spouse is", [], False)
    UNCLE = ('', 'The uncle of <subject> is', [], False)
    AUNT = ('', 'The aunt of <subject> is', [], False)
    CHILD = ('P40', 'The child of <subject> is', ['NUMBER_OF_CHILDREN'], False)
    NUMBER_OF_CHILDREN = ('P1971', 'The number of children <subject> has is', [], True)
    SEX_OR_GENDER = ('P21', "<subject>'s gender is", [], True)
    HEAD_OF_GOVERNMENT = ('P6', 'The head of government of <subject> is', ['head of state'], False)
    COUNTRY = ('P17', 'The country which <subject> is associated with is', [], True)
    PLACE_OF_BIRTH = ('P19', 'The city in which <subject> was born is', ['country of citizenship'], True)
    PLACE_OF_DEATH = ('P20', 'The city in which <subject> died is', ['is alive'], True)
    COUNTRY_OF_CITIZENSHIP = ('P27', 'The country of citizenship of <subject> is', [], False)
    CONTINENT = ('P30', 'The continent which <subject> is part of is', ['country'], True)
    HEAD_OF_STATE = ('P35', 'The head of state of <subject> is', ['head of government'], False)
    CAPITAL = ('P36', 'The capital of <subject> is', [], True)
    CAPITAL_OF = ('P1376', '<subject> is the capital of',
                  ['country', 'continent', 'currency', 'official language', 'anthem'], True)
    CURRENCY = ('P38', 'The currency in <subject> is', [], False)
    POSITION_HELD = ('P39', 'The position that has been held by <subject> is', [], False)
    OFFICIAL_LANGUAGE = ('P37', 'The official language of <subject> is', [], False)
    STEPFATHER = ('P43', 'The stepfather of <subject> is', ['number of children'], True)
    STEPMOTHER = ('P44', 'The stepmother of <subject> is', [], True)
    AUTHOR = ('P50', 'The author of <subject> is', [], False)
    MEMBER_OF_SPORTS_TEAM = ('P54', '<subject> has been a member of a sports team. This team is', [], False)
    DIRECTOR = ('P57', 'The director of <subject> is', [], False)
    SCREENWRITER = ('P58', 'The screenwriter of <subject> is', [], False)
    ALMA_MATER = ('P69', '<subject> has been educated at', [], False)
    ARCHITECT = ('P84', 'The architect of <subject> is', [], False)
    COMPOSER = ('P86', 'The screenwriter of <subject> is', [], False)
    ANTHEM = ('P85', 'The anthem of <subject> is', [], True)
    SEXUAL_ORIENTATION = ('P91', "<subject>'s sexual orientation is", [], False)
    EDITOR = ('P98', 'The editor of <subject> is', [], False)
    OCCUPATION = ('P106', 'The occupation of <subject> is', ['field of work'], False)
    EMPLOYER = ('P108', "<subject>'s employer is", [], False)
    FOUNDER = ('P112', 'The founder of <subject> is', [], False)
    LEAGUE = ('P118', 'The league in which <subject> plays is', [], False)
    PLACE_OF_BURIAL = ('P119', 'The country in which <subject> is buried is', ['is alive'], True)
    FIELD_OF_WORK = ('P101', '<subject> has been working in the field of', ['occupation'], False)
    NATIVE_LANGUAGE = ('P03', 'The mother tongue of <subject> is', [], False)
    CAST_MEMBER = ('P161', "<subject>'s cast members are", [], False)
    AWARD_RECEIVED = ('P166', '<subject> has won the award of', [], False)
    FOLLOWS = ('P155', '<subject> follows', [], True)
    ETHNIC_GROUP = ('P172', 'The ethnic group which <subject> is associated with is', [], False)
    RELIGION = ('P140', 'The religion which <subject> is associated with is', [], False)
    EYE_COLOR = ('P1340', 'The eye color of <subject> is', [], True)
    DATE_OF_BIRTH = ('P569', 'The date in which <subject> was born in is', [], True)
    DATE_OF_DEATH = ('P570', 'The date in which <subject> was died in is', ['is alive'], True)
    IS_ALIVE = ('', 'Is <subject> still alive or is he dead?', ['place of death', 'place of burial', 'date of death'], True)

    def __init__(self, relation_id, phrase, impacted_relations, is_modification):
        self._relation_id = relation_id
        self._phrase = phrase
        self._impacted_relations = impacted_relations
        self._is_modification = is_modification

    def id(self):
        return self._relation_id

    def phrase(self, subject):
        return self._phrase.replace('<subject>', subject)

    def evaluate(self, subject):
        return subject_relation_to_targets(subject, self._relation_id)

    def impacted_relations(self):
        return [self.string_to_enum(r) for r in self._impacted_relations]

    def is_modification(self):
        return self._is_modification

    @staticmethod
    def string_to_enum(relation_name: str):
        processed_relation_name = relation_name.replace(' ', '_')
        for relation in Relation:
            if compute_exact_match(processed_relation_name, relation.name):
                return relation
        return None

    @staticmethod
    def id_to_enum(relation_id: str):
        for relation in Relation:
            if compute_exact_match(relation_id, relation.id()):
                return relation
        return None
