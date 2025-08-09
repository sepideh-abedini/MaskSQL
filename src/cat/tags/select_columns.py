from enum import auto

from src.cat.tag_collector import TagCollector
from src.cat.tag_collector_result import TagCollectorResult
from src.cat.tags.sql_tag import OrderedTag, SqlTag
from src.parse.node import SelectClauseNode, TerminalNode, ResultColumnNode, ColumnNode


class SelectColumns(SqlTag):
    SingleColumn = auto()
    StarColumn = auto()
    MultiColumn = auto()

    @staticmethod
    class Collector(TagCollector):

        def visit_column(self, node: ColumnNode):
            if node.column_name.value == "*":
                return TagCollectorResult(SelectColumns.StarColumn)
            return TagCollectorResult()

        def visit_select_clause(self, node: SelectClauseNode):
            tags = super().visit_select_clause(node)
            if len(node.result_columns) > 1:
                tags += TagCollectorResult(SelectColumns.MultiColumn)
            elif len(node.result_columns) == 1:
                tags += TagCollectorResult(SelectColumns.SingleColumn)
            return tags

            # if len(node.result_columns) == 1:
            #     col = node.result_columns[0].expr
            #     if isinstance(col, TerminalNode) and col.value == "*":
            #         return TagCollectorResult(SelectColumns.SingleStarColumn)
            #     return TagCollectorResult()
            # else:
            #     return TagCollectorResult(SelectColumns.MultiColumn)
