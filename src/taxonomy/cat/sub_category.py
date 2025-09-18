from dataclasses import dataclass, replace
from typing import FrozenSet, Type, Set

from src.taxonomy.cat.tags.sql_tag import SqlTag


@dataclass(eq=True, frozen=True)
class SubCategory:
    name: str
    tags: FrozenSet[SqlTag]
    description: str = ""

    def __ge__(self, other: 'SubCategory'):
        for tag in other.tags:
            if not self.has_greater(tag):
                return False
        return True

    def __lt__(self, other):
        return not (self >= other)

    def has_greater(self, tag: SqlTag):
        for t in self.tags:
            if t >= tag:
                return True
        return False

    def __str__(self):
        return self.name

    def __add__(self, other):
        if isinstance(other, SqlTag):
            return replace(self, tags=self.tags.union({other}))
        if isinstance(other, SubCategory):
            return replace(self, tags=self.tags.union(other.tags))
        raise RuntimeError(f"Invalid add operand type {type(other)}")

    def get_val(self, tag_type: Type[SqlTag]) -> str:
        intersection = self.tags.intersection(tag_type.__members__.values())
        if len(intersection) > 0:
            return next(iter(intersection)).name
        else:
            return 'None'

    # def reduce(self):
    #     """Remove any tag if some other tag harder or equal than it exists"""
    #     to_remove = set()
    #     for t in self.tags:
    #         for ot in self.tags:
    #             if t != ot and ot >= t:
    #                 to_remove.add(t)
    #     return SubCategory(frozenset(self.tags.difference(to_remove)))
    #
    def __repr__(self):
        return str(self)
