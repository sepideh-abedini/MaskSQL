from src.parse.node import *


class NodeVisitor(ABC):

    @abstractmethod
    def visit_select_statement(self, node: SelectStatementNode):
        pass

    @abstractmethod
    def visit_select_core(self, node: SelectCoreNode):
        pass

    @abstractmethod
    def visit_select_clause(self, node: SelectClauseNode):
        pass

    @abstractmethod
    def visit_group_clause(self, node: GroupClauseNode):
        pass

    @abstractmethod
    def visit_from_clause(self, node: FromClauseNode):
        pass

    @abstractmethod
    def visit_where_clause(self, node: WhereClauseNode):
        pass

    @abstractmethod
    def visit_between_expression(self, node: BetweenExpressionNode):
        pass

    @abstractmethod
    def visit_order_by(self, node: OrderByNode):
        pass

    @abstractmethod
    def visit_ordering_term(self, node: OrderingTerm):
        pass

    @abstractmethod
    def visit_limit(self, node: LimitNode):
        pass

    @abstractmethod
    def visit_join_clause(self, node: JoinClauseNode):
        pass

    @abstractmethod
    def visit_join_constraint(self, node: JoinConstraintNode):
        pass

    @abstractmethod
    def visit_table_or_subquery(self, node: TableOrSubqueryNode):
        pass

    @abstractmethod
    def visit_result_column(self, node: ResultColumnNode):
        pass

    @abstractmethod
    def visit_column(self, node: ColumnNode):
        pass

    @abstractmethod
    def visit_function_expression(self, node: FunctionExpressionNode):
        pass

    @abstractmethod
    def visit_bin_op_expression(self, node: BinOpExpressionNode):
        pass

    @abstractmethod
    def visit_terminal(self, node: TerminalNode):
        pass

    @abstractmethod
    def visit_expression(self, node: ExpressionNode):
        pass

    @abstractmethod
    def visit_literal(self, node: LiteralNode):
        pass

    @abstractmethod
    def visit_cast_expression(self, node: CastExpressionNode):
        pass

    @abstractmethod
    def visit_window_expression(self, node: WindowExpressionNode):
        pass

    @abstractmethod
    def visit_window_definition(self, node: WindowDefinitionNode):
        pass

    @abstractmethod
    def visit_literal_list(self, node: LiteralListNode):
        pass

    @abstractmethod
    def visit_with_clause(self, node: WithClauseNode):
        pass

    @abstractmethod
    def visit_common_table_expression(self, node: CommonTableExpressionNode):
        pass
