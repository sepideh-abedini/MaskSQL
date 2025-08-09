from typing import List, Optional

from src.cat.statement_category import StatementCategory
from src.cat.sub_category import SubCategory
from src.cat.tags.complex_keys import ComplexKeywords
from src.cat.tags.expr_type import ExprType
from src.cat.tags.extra import ExtraKeywords
from src.cat.tags.group_cond import GroupType
from src.cat.tags.join_cond import JoinConditions
from src.cat.tags.join_tables import JoinTables
from src.cat.tags.join_type import JoinType, JoinSub
from src.cat.tags.nest_level import NestLevel
from src.cat.tags.select_columns import SelectColumns
from src.cat.tags.structure import StructureType
from src.cat.tags.where_exprs import WhereType

CAT_1 = StatementCategory(
    1,
    SubCategory("s0", frozenset([SelectColumns.SingleColumn]), "Having single column in SELECT clause"),
    SubCategory("s1", frozenset([SelectColumns.MultiColumn]), "Having single column in SELECT clause"),
    SubCategory("s2", frozenset([SelectColumns.StarColumn]), "Having single star column in the SELECT clause"),
    SubCategory("s3", frozenset([ExtraKeywords.OrderBy]), "Having ORDER_BY keyword"),
)

CAT_2 = StatementCategory(
    2,
    SubCategory("s4", frozenset([WhereType.SingleWhereExpr, ExprType.SingleBinExpr]),
                "Having a single binary expression in the where clause"),
    SubCategory("s5", frozenset([ExprType.ArithExpr]), "Only having arithmetic expressions"),
    SubCategory("s6", frozenset([ExtraKeywords.AGGREGATE]), "Having aggregate functions"),
    SubCategory("s7", frozenset([ExtraKeywords.Limit]), "Having LIMIT keyword"),
    SubCategory("s8", frozenset([ExtraKeywords.Distinct]), "Having Distinct Keyword"),
    SubCategory("s9", frozenset([GroupType.UnconditionalGroup]), "Having GROUP BY clause without HAVING clause"),
    SubCategory("s10", frozenset([JoinTables.SingleJoin, JoinType.EquiJoin]), "Having equi-join"),
    SubCategory("s10", frozenset([JoinTables.SingleJoin, JoinType.NaturalJoin]), "Having natural join"),
)

CAT_3 = StatementCategory(
    3,
    SubCategory("s11", frozenset([JoinType.NonEquiJoin]), "Having non-equi-joins"),
    SubCategory("s12", frozenset([ExtraKeywords.BETWEEN]), "Having between expressions"),
    SubCategory("s13", frozenset([JoinConditions.UnconditionalJoin, WhereType.SingleWhereExpr]),
                "Having a JOIN clause without join condition plus having single expression in WHERE clause"),
    SubCategory("s14", frozenset([GroupType.UnconditionalGroup, WhereType.SingleWhereExpr]),
                "Having GROUP BY clause without HAVING clause plus having single expression in WHERE clause"),
    SubCategory("s15",
                frozenset([GroupType.UnconditionalGroup, JoinConditions.UnconditionalJoin]),
                "Having GROUP BY clause without condition plus having JOIN clause without join condition"),
    SubCategory("s16", frozenset([GroupType.ConditionalGroup]), "Having GROUP BY clause without condition"),
    SubCategory("s17", frozenset([ExtraKeywords.LIKE]), "Having like expressions"),
    SubCategory("s18", frozenset([ExtraKeywords.IS_NULL]), "Having is null expressions"),
    SubCategory("s19", frozenset([WhereType.MultipleWhereExpr]), "Having multiple expressions in WHERE clause"),
)

CAT_4 = StatementCategory(
    4,
    SubCategory("s20", frozenset([NestLevel.One]), "Having exactly one level of nested queries"),
    SubCategory("s21", frozenset([StructureType.Compound]), "Having a composition keyword such as INTERSECT or UNION"),
    SubCategory("s25", frozenset([JoinTables.MultiJoin]), "Having more than two joins"),
    SubCategory("s23", frozenset([NestLevel.One, ExtraKeywords.EXISTS]),
                "Having nested subqueries with Exists expressions"),
    SubCategory("s24", frozenset([NestLevel.One, ExtraKeywords.IN]),
                "Having nested subqueries with IN expressions"),
    SubCategory("s22", frozenset([JoinType.NonSimpleJoin]), "Having inner,outer joins")
)

CAT_4_NEW = StatementCategory(
    4,
    SubCategory("s20", frozenset([NestLevel.One]), "Having exactly one level of nested queries"),
    SubCategory("s21", frozenset([StructureType.Compound]), "Having a composition keyword such as INTERSECT or UNION"),
    SubCategory("s22", frozenset([NestLevel.One, ExtraKeywords.IN]),
                "Having nested subqueries with IN expressions"),
    SubCategory("s23", frozenset([JoinType.NonSimpleJoin, JoinSub.INNER]),
                "Having Inner Join"),
    SubCategory("s24", frozenset([JoinType.NonSimpleJoin, ExtraKeywords.OrderBy]),
                "Having a non-simple join with Order By"),
    SubCategory("s25", frozenset([JoinType.NonSimpleJoin, GroupType.UnconditionalGroup]),
                "Having a non-simple join with unconditional group by"),
    SubCategory("s26", frozenset([JoinType.NonSimpleJoin, ExtraKeywords.AGGREGATE]),
                "Having a non-simple join with aggregation keyword"),
    SubCategory("s27", frozenset([JoinTables.MultiJoin]), "Having more than two joins"),
)

CAT_5 = StatementCategory(
    5,
    SubCategory("s28", frozenset([StructureType.Nested, GroupType.UnconditionalGroup]),
                "Having nested sub-queries plus having GROUP BY clause without condition"),
    SubCategory("s29", frozenset([StructureType.Nested, JoinConditions.UnconditionalJoin]),
                "Having nested sub-queries plus with a join clause without a condition"),
    SubCategory("s30", frozenset([StructureType.Nested, ExtraKeywords.AGGREGATE]),
                "Having nested sub-queries plus with aggregate functions"),
    SubCategory("s31", frozenset([NestLevel.Two]), "Having exactly two level of nested sub-queries")
)

CAT_6 = StatementCategory(
    6,
    SubCategory("s32", frozenset([NestLevel.Many]), "Having more than two level of nested sub-queries"),
    SubCategory("s33", frozenset([StructureType.Compound, StructureType.Nested]),
                "Having a composition keyword such as (INTERSECT or UNION) and having nested sub-queries"),
    SubCategory("s34", frozenset([ComplexKeywords.CaseExpr]),
                "Having case expressions"),
    SubCategory("s35", frozenset([ComplexKeywords.CTE]),
                "Having a cte"),
    SubCategory("s36", frozenset([ComplexKeywords.WindowFunction]),
                "Having a window function"),
)

CAT_INF = StatementCategory(1000)
SUB_INF = SubCategory("s100", frozenset(), "Inf complexity")

CATS = [CAT_1, CAT_2, CAT_3, CAT_4_NEW, CAT_5, CAT_6]


def get_all_sub_cats(cats: List[StatementCategory]):
    sub_cats = []
    for cat in cats:
        for sub_cat in cat.sub_cats:
            # sub_cat_full_name = f"{cat.name}_{sub_cat.name}"
            sub_cat_full_name = f"{sub_cat.name}"
            sub_cats.append(sub_cat_full_name)
    return sub_cats


def get_all_cats(cats: List[StatementCategory]):
    return list(map(lambda c: c.name, cats))


def find_sub(cat_name: str) -> Optional[SubCategory]:
    for c in CATS:
        for s in c.sub_cats:
            if s.name == cat_name:
                return s
    return SUB_INF


def find_cat(cat_name: str) -> Optional[StatementCategory]:
    for c in CATS:
        if c.name == cat_name:
            return c
    return CAT_INF
