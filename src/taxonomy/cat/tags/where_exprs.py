from src.taxonomy.cat.tag_collector import TagCollector
from src.taxonomy.cat.tag_collector_result import TagCollectorResult
from src.taxonomy.cat.tags.sql_tag import OrderedTag
from src.taxonomy.parse.node import WhereClauseNode, BinOpExpressionNode


class WhereType(OrderedTag):
    SingleWhereExpr = 1
    MultipleWhereExpr = 2

    @staticmethod
    class Collector(TagCollector):
        is_where_expr: bool = False

        def visit_where_clause(self, node: WhereClauseNode):
            self.is_where_expr = True
            tags = super().visit_where_clause(node)
            self.is_where_expr = False
            return tags

        def visit_bin_op_expression(self, node: BinOpExpressionNode):
            if not self.is_where_expr:
                return TagCollectorResult()
            tags = super().visit_bin_op_expression(node)
            if node.op.value.lower() not in ['and', 'or']:
                tags += TagCollectorResult(WhereType.SingleWhereExpr)
            else:
                tags += TagCollectorResult(WhereType.MultipleWhereExpr)
            return tags
