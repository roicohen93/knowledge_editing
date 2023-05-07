from relation import Relation


relation_relation2phrase = {
    f'{Relation.MOTHER.name}-{Relation.MOTHER.name}': "The maternal grandmother of <subject> is",
    f'{Relation.MOTHER.name}-{Relation.FATHER.name}': "The maternal grandfather of <subject> is",
    f'{Relation.Father.name}-{Relation.MOTHER.name}': "The paternal grandmother of <subject> is",
    f'{Relation.Father.name}-{Relation.FATHER.name}': "The paternal grandfather of <subject> is",
}


def relation_couple_to_key(relation1: Relation, relation2: Relation):
    return f'{relation1.name}-{relation2.name}'
