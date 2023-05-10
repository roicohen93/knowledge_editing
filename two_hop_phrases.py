from relation import Relation

relation_relation2phrase = {

    f'{Relation.MOTHER.name}-{Relation.MOTHER.name}': "The maternal grandmother of <subject> is",
    f'{Relation.MOTHER.name}-{Relation.FATHER.name}': "The maternal grandfather of <subject> is",
    f'{Relation.MOTHER.name}-{Relation.BROTHER.name}': "The maternal uncle of <subject> is",
    f'{Relation.MOTHER.name}-{Relation.SISTER.name}': "The maternal aunt of <subject> is",
    f'{Relation.MOTHER.name}-{Relation.SIBLING.name}': "The sibling of <subject>'s mother is",
    f'{Relation.MOTHER.name}-{Relation.SPOUSE.name}': "The spouse of <subject>'s mother is",
    f'{Relation.MOTHER.name}-{Relation.UNCLE.name}': "The maternal great uncle of <subject> is",
    f'{Relation.MOTHER.name}-{Relation.AUNT.name}': "The maternal great aunt of <subject> is",
    f'{Relation.MOTHER.name}-{Relation.CHILD.name}': "The child of <subject>'s mother is",
    f'{Relation.MOTHER.name}-{Relation.NUMBER_OF_CHILDREN.name}': "The number of children <subject>'s mother has is",
    f'{Relation.MOTHER.name}-{Relation.SEX_OR_GENDER.name}': "The gender of <subject>'s mother is",
    f'{Relation.MOTHER.name}-{Relation.PLACE_OF_BIRTH.name}': "The place of birth of <subject>'s mother is",
    f'{Relation.MOTHER.name}-{Relation.PLACE_OF_DEATH.name}': "The place of death of <subject>'s mother is",
    f'{Relation.MOTHER.name}-{Relation.COUNTRY.name}': "The country which <subject>'s mother is associated with is",
    f'{Relation.MOTHER.name}-{Relation.COUNTRY_OF_CITIZENSHIP.name}': "The country of citizenship of <subject>'s mother is",

    f'{Relation.FATHER.name}-{Relation.MOTHER.name}': "The paternal grandmother of <subject> is",
    f'{Relation.FATHER.name}-{Relation.FATHER.name}': "The paternal grandfather of <subject> is",
    f'{Relation.FATHER.name}-{Relation.BROTHER.name}': "The paternal uncle of <subject> is",
    f'{Relation.FATHER.name}-{Relation.SISTER.name}': "The paternal aunt of <subject> is",
    f'{Relation.FATHER.name}-{Relation.SIBLING.name}': "The sibling of <subject>'s father is",
    f'{Relation.FATHER.name}-{Relation.SPOUSE.name}': "The spouse of <subject>'s father is",
    f'{Relation.FATHER.name}-{Relation.UNCLE.name}': "The paternal great uncle of <subject> is",
    f'{Relation.FATHER.name}-{Relation.AUNT.name}': "The paternal great aunt of <subject> is",
    f'{Relation.FATHER.name}-{Relation.CHILD.name}': "The child of <subject>'s father is",
    f'{Relation.FATHER.name}-{Relation.NUMBER_OF_CHILDREN.name}': "The number of children <subject>'s father has is",
    f'{Relation.FATHER.name}-{Relation.SEX_OR_GENDER.name}': "The gender of <subject>'s father is",
    f'{Relation.FATHER.name}-{Relation.PLACE_OF_BIRTH.name}': "The place of birth of <subject>'s father is",
    f'{Relation.FATHER.name}-{Relation.PLACE_OF_DEATH.name}': "The place of death of <subject>'s father is",
    f'{Relation.FATHER.name}-{Relation.COUNTRY.name}': "The country which <subject>'s father is associated with is",
    f'{Relation.FATHER.name}-{Relation.COUNTRY_OF_CITIZENSHIP.name}': "The country of citizenship of <subject>'s father is",

    f'{Relation.SPOUSE.name}-{Relation.MOTHER.name}': "The mother in law of <subject> is",
    f'{Relation.SPOUSE.name}-{Relation.FATHER.name}': "The father in law of <subject> is",
    f'{Relation.SPOUSE.name}-{Relation.BROTHER.name}': "The brother in law of <subject> is",
    f'{Relation.SPOUSE.name}-{Relation.SISTER.name}': "The sister in law of <subject> is",
    f'{Relation.SPOUSE.name}-{Relation.SIBLING.name}': "The sibling in law of <subject> is",
    f'{Relation.SPOUSE.name}-{Relation.UNCLE.name}': "The uncle in law of <subject> is",
    f'{Relation.SPOUSE.name}-{Relation.AUNT.name}': "The aunt in law of <subject> is",
    f'{Relation.SPOUSE.name}-{Relation.CHILD.name}': "The child of <subject>'s spouse is",
    f'{Relation.SPOUSE.name}-{Relation.NUMBER_OF_CHILDREN.name}': "The number of children <subject>'s spouse has is",
    f'{Relation.SPOUSE.name}-{Relation.SEX_OR_GENDER.name}': "The gender of <subject>'s spouse is",
    f'{Relation.SPOUSE.name}-{Relation.PLACE_OF_BIRTH.name}': "The place of birth of <subject>'s spouse is",
    f'{Relation.SPOUSE.name}-{Relation.PLACE_OF_DEATH.name}': "The place of death of <subject>'s spouse is",
    f'{Relation.SPOUSE.name}-{Relation.COUNTRY.name}': "The country which <subject>'s spouse is associated with is",
    f'{Relation.SPOUSE.name}-{Relation.COUNTRY_OF_CITIZENSHIP.name}': "The country of citizenship of <subject>'s spouse is",

    f'{Relation.HEAD_OF_GOVERNMENT.name}-{Relation.MOTHER.name}': "The mother of <subject>'s head of government is",
    f'{Relation.HEAD_OF_GOVERNMENT.name}-{Relation.FATHER.name}': "The father of <subject>'s head of government is",
    f'{Relation.HEAD_OF_GOVERNMENT.name}-{Relation.BROTHER.name}': "The brother of <subject>'s head of government is",
    f'{Relation.HEAD_OF_GOVERNMENT.name}-{Relation.SISTER.name}': "The sister of <subject>'s head of government is",
    f'{Relation.HEAD_OF_GOVERNMENT.name}-{Relation.SIBLING.name}': "The sibling of <subject>'s head of government is",
    f'{Relation.HEAD_OF_GOVERNMENT.name}-{Relation.SPOUSE.name}': "The spouse of <subject>'s head of government is",
    f'{Relation.HEAD_OF_GOVERNMENT.name}-{Relation.UNCLE.name}': "The uncle of <subject>'s head of government is",
    f'{Relation.HEAD_OF_GOVERNMENT.name}-{Relation.AUNT.name}': "The aunt of <subject>'s head of government is",
    f'{Relation.HEAD_OF_GOVERNMENT.name}-{Relation.CHILD.name}': "The child of <subject>'s head of government is",
    f'{Relation.HEAD_OF_GOVERNMENT.name}-{Relation.NUMBER_OF_CHILDREN.name}': "The number of children <subject>'s head of government has is",
    f'{Relation.HEAD_OF_GOVERNMENT.name}-{Relation.SEX_OR_GENDER.name}': "The gender of <subject>'s head of government is",
    f'{Relation.HEAD_OF_GOVERNMENT.name}-{Relation.PLACE_OF_BIRTH.name}': "The place of birth of <subject>'s head of government is",
    f'{Relation.HEAD_OF_GOVERNMENT.name}-{Relation.COUNTRY.name}': "The country which <subject>'s head of government is associated with is",
    f'{Relation.HEAD_OF_GOVERNMENT.name}-{Relation.COUNTRY_OF_CITIZENSHIP.name}': "The country of citizenship of <subject>'s head of government is",

    f'{Relation.HEAD_OF_STATE.name}-{Relation.MOTHER.name}': "The mother of <subject>'s head of state is",
    f'{Relation.HEAD_OF_STATE.name}-{Relation.FATHER.name}': "The father of <subject>'s head of state is",
    f'{Relation.HEAD_OF_STATE.name}-{Relation.BROTHER.name}': "The brother of <subject>'s head of state is",
    f'{Relation.HEAD_OF_STATE.name}-{Relation.SISTER.name}': "The sister of <subject>'s head of state is",
    f'{Relation.HEAD_OF_STATE.name}-{Relation.SIBLING.name}': "The sibling of <subject>'s head of state is",
    f'{Relation.HEAD_OF_STATE.name}-{Relation.SPOUSE.name}': "The spouse of <subject>'s head of state is",
    f'{Relation.HEAD_OF_STATE.name}-{Relation.UNCLE.name}': "The uncle of <subject>'s head of state is",
    f'{Relation.HEAD_OF_STATE.name}-{Relation.AUNT.name}': "The aunt of <subject>'s head of state is",
    f'{Relation.HEAD_OF_STATE.name}-{Relation.CHILD.name}': "The child of <subject>'s head of state is",
    f'{Relation.HEAD_OF_STATE.name}-{Relation.NUMBER_OF_CHILDREN.name}': "The number of children <subject>'s head of state has is",
    f'{Relation.HEAD_OF_STATE.name}-{Relation.SEX_OR_GENDER.name}': "The gender of <subject>'s head of state is",
    f'{Relation.HEAD_OF_STATE.name}-{Relation.PLACE_OF_BIRTH.name}': "The place of birth of <subject>'s head of state is",
    f'{Relation.HEAD_OF_STATE.name}-{Relation.COUNTRY.name}': "The country which <subject>'s head of state is associated with is",
    f'{Relation.HEAD_OF_STATE.name}-{Relation.COUNTRY_OF_CITIZENSHIP.name}': "The country of citizenship of <subject>'s head of state is",

    f'{Relation.PLACE_OF_BIRTH.name}-{Relation.HEAD_OF_GOVERNMENT.name}': "The head of goverment of <subject>'s place of birth is",
    f'{Relation.PLACE_OF_BIRTH.name}-{Relation.HEAD_OF_STATE.name}': "The head of state of <subject>'s place of birth is",
    f'{Relation.PLACE_OF_BIRTH.name}-{Relation.CONTINENT.name}': "The continent of <subject>'s place of birth is",

    f'{Relation.PLACE_OF_DEATH.name}-{Relation.HEAD_OF_GOVERNMENT.name}': "The head of goverment of <subject>'s place of death is",
    f'{Relation.PLACE_OF_DEATH.name}-{Relation.HEAD_OF_STATE.name}': "The head of state of <subject>'s place of death is",
    f'{Relation.PLACE_OF_DEATH.name}-{Relation.CONTINENT.name}': "The continent of <subject>'s place of death is",

    f'{Relation.COUNTRY.name}-{Relation.HEAD_OF_GOVERNMENT.name}': "The head of goverment of the country which <subject> is associated with is",
    f'{Relation.COUNTRY.name}-{Relation.HEAD_OF_STATE.name}': "The head of state of the country which <subject> is associated with is",
    f'{Relation.COUNTRY.name}-{Relation.CONTINENT.name}': "The continent of the country which <subject> is associated with is",

    f'{Relation.COUNTRY_OF_CITIZENSHIP.name}-{Relation.HEAD_OF_GOVERNMENT.name}': "The head of goverment of <subject>'s country of citizenship is",
    f'{Relation.COUNTRY_OF_CITIZENSHIP.name}-{Relation.HEAD_OF_STATE.name}': "The head of state of <subject>'s country of citizenship is",
    f'{Relation.COUNTRY_OF_CITIZENSHIP.name}-{Relation.CONTINENT.name}': "The continent of <subject>'s country of citizenship is",

}


def relation_couple_to_key(relation1: Relation, relation2: Relation):
    return f'{relation1.name}-{relation2.name}'


def relation_couple_to_phrase(relation1: Relation, relation2: Relation):
    key_for_dict = relation_couple_to_key(relation1, relation2)
    if key_for_dict not in relation_relation2phrase:
        return None
    return relation_relation2phrase[key_for_dict]
