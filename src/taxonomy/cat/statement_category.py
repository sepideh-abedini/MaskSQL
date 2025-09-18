from typing import Set

from src.taxonomy.cat.sub_category import SubCategory


class StatementCategory:
    rank: int
    sub_cats: Set[SubCategory]

    def __init__(self, rank: int, *tag_sets: SubCategory):
        self.rank = rank
        self.sub_cats = set(tag_sets)

    @property
    def name(self):
        return f"c{self.rank}"

    def __str__(self):
        return self.name

    def __le__(self, other):
        if not isinstance(other, StatementCategory):
            raise RuntimeError(f"Invalid operand: {type(other)}")
        return self.rank <= other.rank

    def matches(self, feature_set: SubCategory):
        matchs = []
        for fs in self.sub_cats:
            if feature_set >= fs:
                matchs.append(fs)
        if len(matchs) > 0:
            return matchs
        return None
