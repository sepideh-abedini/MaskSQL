from src.taxonomy.cat.tag_collector import TagCollector
from src.taxonomy.cat.tag_collector_result import TagCollectorResult
from src.taxonomy.cat.tags.sql_tag import OrderedTag
from src.taxonomy.parse.node import BinOpExpressionNode, BetweenExpressionNode


class ExprType(OrderedTag):
    SingleBinExpr = 1
    ArithExpr = 2
    ComplexExpr = 3

    @staticmethod
    class Collector(TagCollector):
        def visit_bin_op_expression(self, node: BinOpExpressionNode):
            tags = super().visit_bin_op_expression(node)
            if node.is_arith_expr():
                return tags + TagCollectorResult(ExprType.ArithExpr)
            else:
                if ((isinstance(node.left, str) or not node.left.has_sub_expr()) and
                        (isinstance(node.right, str) or not node.right.has_sub_expr())):
                    return tags + TagCollectorResult(ExprType.SingleBinExpr)
                else:
                    return tags + TagCollectorResult(ExprType.ComplexExpr)

        def visit_between_expression(self, node: BetweenExpressionNode):
            tags = super().visit_between_expression(node)
            return tags + TagCollectorResult(ExprType.ComplexExpr)
