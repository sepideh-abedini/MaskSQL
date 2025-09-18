from dataclasses import fields
from typing import Any, Type

from src.taxonomy.parse.node import *
from src.taxonomy.parse.visitor.node_visitor import NodeVisitor
from src.taxonomy.parse.visitor.visitor_result import MergeableVisitorResult


class CollectorVisitor(NodeVisitor):
    """Automatically visits all attributes of a node and
    merges the results."""

    def __init__(self, result_class: Type[MergeableVisitorResult]):
        super().__init__()
        self.result_class = result_class

    def visit_literal_list(self, node: LiteralListNode):
        return self.visit_node(node)

    def visit_with_clause(self, node: WithClauseNode):
        return self.visit_node(node)

    def visit_common_table_expression(self, node: CommonTableExpressionNode):
        return self.visit_node(node)

    def visit_window_expression(self, node: WindowExpressionNode):
        return self.visit_node(node)

    def visit_window_definition(self, node: WindowDefinitionNode):
        return self.visit_node(node)

    def visit_cast_expression(self, node: CastExpressionNode):
        return self.visit_node(node)

    def get_new_result_instance(self, attr: Any):
        return self.result_class()

    def get_attrs(self, node: SqlAstNode):
        attrs = []
        for f in fields(node.__class__):
            attr = node.__getattribute__(f.name)
            if type(attr) is list:
                attrs += attr
            else:
                attrs += [attr]
        return attrs

    def visit_node(self, node):
        """Dynamically visit all attributes of the node"""
        data = self.get_new_result_instance(node)
        attrs = self.get_attrs(node)
        for attr in attrs:
            data += self.visit_attr(attr)
        return data

    def visit_attr(self, attr):
        """Visit the attribute if it is an instance of AstNode,
        otherwise return an instance of result class"""
        if attr and isinstance(attr, SqlAstNode):
            return attr.accept(self)
        else:
            return self.get_new_result_instance(attr)

    def visit_ordering_term(self, node: OrderingTerm):
        return self.visit_node(node)

    def visit_select_statement(self, node: SelectStatementNode):
        return self.visit_node(node)

    def visit_select_core(self, node: SelectCoreNode):
        return self.visit_node(node)

    def visit_select_clause(self, node: SelectClauseNode):
        return self.visit_node(node)

    def visit_from_clause(self, node: FromClauseNode):
        return self.visit_node(node)

    def visit_join_clause(self, node: JoinClauseNode):
        return self.visit_node(node)

    def visit_table_or_subquery(self, node: TableOrSubqueryNode):
        return self.visit_node(node)

    def visit_result_column(self, node: ResultColumnNode):
        return self.visit_node(node)

    def visit_column(self, node: ColumnNode):
        return self.visit_node(node)

    def visit_where_clause(self, node: WhereClauseNode):
        return self.visit_node(node)

    def visit_group_clause(self, node: GroupClauseNode):
        return self.visit_node(node)

    def visit_between_expression(self, node: BetweenExpressionNode):
        return self.visit_node(node)

    def visit_order_by(self, node: OrderByNode):
        return self.visit_node(node)

    def visit_limit(self, node: LimitNode):
        return self.visit_node(node)

    def visit_join_constraint(self, node: JoinConstraintNode):
        return self.visit_node(node)

    def visit_function_expression(self, node: FunctionExpressionNode):
        return self.visit_node(node)

    def visit_bin_op_expression(self, node: BinOpExpressionNode):
        return self.visit_node(node)

    def visit_terminal(self, node: TerminalNode):
        return self.visit_node(node)

    def visit_expression(self, node: ExpressionNode):
        return self.visit_node(node)

    def visit_literal(self, node: LiteralNode):
        return self.visit_node(node)
