from enum import auto

from src.cat.tag_collector import TagCollector
from src.cat.tag_collector_result import TagCollectorResult
from src.cat.tags.sql_tag import SqlTag
from src.parse.node import WithClauseNode, WindowExpressionNode, FunctionExpressionNode


class ComplexKeywords(SqlTag):
    CTE = auto()
    WindowFunction = auto()
    CaseExpr = auto()

    @staticmethod
    class Collector(TagCollector):

        def visit_with_clause(self, node: WithClauseNode):
            tags = super().visit_with_clause(node)
            tags += TagCollectorResult(ComplexKeywords.CTE)
            return tags

        def visit_window_expression(self, node: WindowExpressionNode):
            tags = super().visit_window_expression(node)
            tags += TagCollectorResult(ComplexKeywords.WindowFunction)
            return tags

        def visit_function_expression(self, node: FunctionExpressionNode):
            tags = super().visit_function_expression(node)
            if node.fun_name.value.lower() == "case":
                tags += TagCollectorResult(ComplexKeywords.CaseExpr)
            return tags
