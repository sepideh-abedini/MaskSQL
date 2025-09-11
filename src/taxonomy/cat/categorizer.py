from typing import List

from natsort import natsorted

from src.cat.categories import CAT_1, CAT_2, CAT_3, CAT_4, CAT_5, CAT_6, CATS, CAT_INF, SUB_INF
from src.cat.statement_category import StatementCategory
from src.cat.sub_category import SubCategory


class Categorizer:
    categories: List[StatementCategory]

    def __init__(self, categories=None):
        if categories is None:
            categories = CATS
        self.categories = categories

    def get_category(self, tag_set: SubCategory):
        for c in reversed(
                self.categories):  # Check to find a match starting from
            # harder categories
            sub_cat = c.matches(tag_set)
            if sub_cat:
                # return f"{c.name}_{sub_cat.name}"
                # return f"{sub_cat.name}"
                # return f"{c.name}"
                return c
        return CAT_INF

    def get_sub_category(self, tag_set: SubCategory):
        matched_sub_cats = []
        for c in reversed(self.categories):  # Check to find a match starting from
            # harder categories
            sub_cats = c.matches(tag_set)
            if sub_cats:
                sorted_sub_cats = natsorted(sub_cats, key=lambda s: s.name)
                return sorted_sub_cats[-1]
                # return f"{c.name}_{sub_cat.name}"
                # return f"{sub_cat.name}"
                # return f"{c.name}"

        return SUB_INF
