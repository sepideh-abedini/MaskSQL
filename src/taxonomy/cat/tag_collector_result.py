from typing import Set

from src.cat.sub_category import SubCategory

from src.cat.tags.sql_tag import SqlTag
from src.parse.visitor.visitor_result import MergeableVisitorResult


class TagCollectorResult(MergeableVisitorResult):
    tag_set: SubCategory
    extras: Set[str]

    def __init__(self, *tags: SqlTag):
        self.tag_set = SubCategory('', frozenset([*tags]))
        self.extras = set()

    def merge(self, other):
        if isinstance(other, TagCollectorResult):
            self.tag_set += other.tag_set
        return self

    def add(self, tag: SqlTag):
        self.tag_set += tag

    def add_extra(self, s):
        self.extras.add(s)

    def __str__(self):
        return str(self.tag_set)
