from dataclasses import dataclass
from enum import auto

from src.cat.tag_collector import TagCollector
from src.cat.tag_collector_result import TagCollectorResult
from src.cat.tags.sql_tag import SqlTag
from src.parse.node import JoinClauseNode, JoinConstraintNode, BinOpExpressionNode


class JoinSub(SqlTag):
    INNER = 0
    OUTER = 1
    LEFT = 2
    RIGHT = 3


class JoinType(SqlTag):
    NaturalJoin = 0
    EquiJoin = 1
    NonEquiJoin = 2
    NonSimpleJoin = 3

    @staticmethod
    class Collector(TagCollector):

        def visit_join_clause(self, node: JoinClauseNode):
            tags = super().visit_join_clause(node)
            if all(constr is None for constr in node.constraints):
                tags += TagCollectorResult(JoinType.NaturalJoin)
            if any(op.value.lower() != "join" for op in node.ops):
                tags += TagCollectorResult(JoinType.NonSimpleJoin)
            for op in node.ops:
                if "inner" in op.value.lower():
                    tags += TagCollectorResult(JoinSub.INNER)
                if "outer" in op.value.lower():
                    tags += TagCollectorResult(JoinSub.OUTER)
                if "left" in op.value.lower():
                    tags += TagCollectorResult(JoinSub.LEFT)
                if "right" in op.value.lower():
                    tags += TagCollectorResult(JoinSub.RIGHT)
            return tags

        def visit_join_constraint(self, node: JoinConstraintNode):
            if isinstance(node.expr, BinOpExpressionNode):
                if node.expr.op.value == "=":
                    return TagCollectorResult(JoinType.EquiJoin)
            return TagCollectorResult(JoinType.NonEquiJoin)
