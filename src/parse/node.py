from abc import ABC, abstractmethod
from dataclasses import dataclass, replace
from typing import Optional, Union, Tuple, List, Set, Dict

from loguru import logger

from src.parse.database_schema import DatabaseSchemaSqlyzr


class SqlAstNode(ABC):
    id: int
    db_id: str
    raw_sql: str
    question: str
    db_schema: DatabaseSchemaSqlyzr
    cols: Set[str]

    @abstractmethod
    def accept(self, visitor):
        pass

    def log_self(self):
        # logger.debug(f"{self.__class__.__name__}: {str(self)}")
        pass

    def __hash__(self):
        return 1


@dataclass
class TerminalNode(SqlAstNode):
    name: str
    value: str

    def accept(self, visitor):
        return visitor.visit_terminal(self)

    def __eq__(self, other):
        if not isinstance(other, TerminalNode):
            return False
        if self.name == other.name and self.value == other.value:
            return True
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


class ExpressionNode(SqlAstNode, ABC):
    def has_sub_expr(self):
        return False


@dataclass
class BinOpExpressionNode(ExpressionNode):
    left: ExpressionNode
    op: TerminalNode
    right: ExpressionNode

    def has_sub_expr(self):
        return True

    def left_and_right_terminal(self):
        return ((isinstance(self.left, str) or not self.left.has_sub_expr()) and
                (isinstance(self.right, str) or not self.right.has_sub_expr()))

    def is_arith_expr(self):
        if self.left_and_right_terminal() and self.op.value in "/*+-":
            return True
        return (isinstance(self.left, BinOpExpressionNode) and self.left.is_arith_expr()) or (
                isinstance(self.right, BinOpExpressionNode) and self.right.is_arith_expr())

    def accept(self, visitor):
        return visitor.visit_bin_op_expression(self)

    def __eq__(self, other):
        if not isinstance(other, BinOpExpressionNode):
            return False

        if (self.op.value == '>' and other.op.value == '<') or (self.op.value == '>=' and other.op.value == '<='):
            return (self.left == other.right) and (self.right == other.left)
        elif (self.op.value == '<' and other.op.value == '>') or (self.op.value == '<=' and other.op.value == '>='):
            return (self.left == other.right) and (self.right == other.left)
        elif (self.op.value == '=' and other.op.value == '=') or (self.op.value == '!=' and other.op.value == '!='):
            return ((self.left == other.left) and (self.right == other.right)) or (
                    (self.left == other.right) and (self.right == other.left))
        elif self.op.value == other.op.value:
            return (self.left == other.left) and (self.right == other.right)
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


@dataclass
# TODO : adding NOT BETWEEN
class BetweenExpressionNode(ExpressionNode):
    expr: ExpressionNode
    lower: ExpressionNode
    upper: ExpressionNode

    def has_sub_expr(self):
        return True

    def accept(self, visitor):
        return visitor.visit_between_expression(self)

    def __eq__(self, other):
        if not isinstance(other, BetweenExpressionNode):
            return False
        if self.expr == other.expr:
            return self.lower == other.lower and self.upper == other.upper
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


@dataclass
class FunctionExpressionNode(ExpressionNode):
    fun_name: TerminalNode
    expr: List[ExpressionNode]
    negation: bool = False  # Used when not of function used NOT EXISTS
    distinct: bool = False

    def has_sub_expr(self):
        return True

    def accept(self, visitor):
        return visitor.visit_function_expression(self)

    def __eq__(self, other):
        if not isinstance(other, FunctionExpressionNode):
            return False
        if self.fun_name == other.fun_name and self.expr == other.expr and \
                self.negation == other.negation:  # and self.distinct == other.distinct:
            return True
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


@dataclass
class ColumnNode(ExpressionNode):
    column_name: TerminalNode
    table_name: Optional[TerminalNode] = None

    def accept(self, visitor):
        return visitor.visit_column(self)

    def exists_in_foreign_keys(self, node: 'ColumnNode'):
        for foreign_key_set in self.db_schema.foreign_keys:
            if node.table_name and (node.table_name.value, node.column_name.value) in foreign_key_set:
                return True
        return False

    def __eq__(self, other):
        if not isinstance(other, ColumnNode):
            return False
        if (self.column_name == other.column_name and self.table_name == other.table_name) or (
                self.exists_in_foreign_keys(self) and self.exists_in_foreign_keys(other)
        ):
            return True
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


@dataclass
class LiteralNode(ExpressionNode):
    value: Union[int, str, ExpressionNode]

    def accept(self, visitor):
        return visitor.visit_literal(self)

    def __eq__(self, other):
        return True
        # if not isinstance(other, LiteralNode):
        #     return True
        # # if self.value == other.value:
        # #     return True
        # else:
        #     return True

    def __hash__(self):
        return 1


@dataclass
class LiteralListNode(ExpressionNode):
    literals: List[LiteralNode]

    def accept(self, visitor):
        return visitor.visit_literal_list(self)

    def __add__(self, other):
        if isinstance(other, LiteralNode):
            return replace(self, literals=self.literals + [other])
        else:
            raise RuntimeError("Invalid operand type: {}".format(type(other)))

    def __eq__(self, other):
        if not isinstance(other, LiteralListNode):
            return False
        else:
            if set(self.literals) == set(other.literals):
                return True
            return False

    def __hash__(self):
        return 1


@dataclass
# 4
class ResultColumnNode(SqlAstNode):
    expr: ExpressionNode
    column_alias: Optional[TerminalNode] = None

    def accept(self, visitor):
        return visitor.visit_result_column(self)

    def __eq__(self, other):
        if not isinstance(other, ResultColumnNode):
            return False
        if self.expr == other.expr and self.column_alias == other.column_alias:
            return True
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


@dataclass
# 3
class SelectClauseNode(SqlAstNode):
    result_columns: List[ResultColumnNode]
    distinct: bool = False

    def accept(self, visitor):
        return visitor.visit_select_clause(self)

    def __add__(self, other):
        if isinstance(other, ResultColumnNode):
            return replace(self, result_columns=self.result_columns + [other])
        else:
            raise RuntimeError("Invalid operand type: {}".format(type(other)))

    def __eq__(self, other):
        if not isinstance(other, SelectClauseNode):
            return False
        if set(self.result_columns) == set(other.result_columns):  # and self.distinct == other.distinct:
            return True
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


@dataclass
class TableOrSubqueryNode(SqlAstNode):
    schema_name: Optional[TerminalNode] = None
    table_name: Optional[TerminalNode] = None  # none or one object
    select_statement: Optional['SelectStatementNode'] = None
    table_alias: Optional[TerminalNode] = None
    join_clause: Optional['JoinClauseNode'] = None

    def accept(self, visitor):
        return visitor.visit_table_or_subquery(self)

    def __eq__(self, other):
        if not isinstance(other, TableOrSubqueryNode):
            return False
        if self.table_name == other.table_name and self.schema_name == other.schema_name and self.select_statement == other.select_statement and self.join_clause == other.join_clause:
            return True
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


@dataclass
class JoinConstraintNode(SqlAstNode):
    expr: ExpressionNode

    def accept(self, visitor):
        return visitor.visit_join_constraint(self)

    def __eq__(self, other):
        if not isinstance(other, JoinConstraintNode):
            return False
        if self.expr == other.expr:
            return True
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


@dataclass
class JoinClauseNode(SqlAstNode):
    tables: List[TableOrSubqueryNode]
    ops: List[TerminalNode]
    constraints: List[Optional[JoinConstraintNode]]

    def add_table(self, table_or_subquery: TableOrSubqueryNode, op: TerminalNode,
                  constraint: Optional[JoinConstraintNode]):
        return replace(self, tables=self.tables + [table_or_subquery],
                       ops=self.ops + [op],
                       constraints=self.constraints + [constraint])

    def accept(self, visitor):
        return visitor.visit_join_clause(self)

    def __eq__(self, other):
        if not isinstance(other, JoinClauseNode):
            return False
        if set(self.tables) == set(other.tables) and self.ops == other.ops and self.constraints == other.constraints:
            return True
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


@dataclass
class OrderingTerm(SqlAstNode):
    expr: ExpressionNode
    sort_order: Optional[TerminalNode] = None  # ascending or descending

    def accept(self, visitor):
        return visitor.visit_ordering_term(self)

    def __eq__(self, other):
        if not isinstance(other, OrderingTerm):
            return False
        if self.expr == other.expr:
            # handling the case of having asc in pred and None in gold or reverse
            if (self.sort_order != None and other.sort_order != None) and \
                    self.sort_order.value != other.sort_order.value:
                return False
            elif (self.sort_order != None and other.sort_order == None) and self.sort_order.value == 'desc':
                return False
            elif (self.sort_order == None and other.sort_order != None) and other.sort_order.value == 'desc':
                return False
            else:
                return True
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


@dataclass
class OrderByNode(SqlAstNode):
    ordering_terms: List[OrderingTerm]

    def accept(self, visitor):
        return visitor.visit_order_by(self)

    def __add__(self, other):
        if isinstance(other, OrderingTerm):
            return replace(self, ordering_terms=self.ordering_terms + [other])
        else:
            raise RuntimeError("Invalid operand type: {}".format(type(other)))

    def __eq__(self, other):
        if not isinstance(other, OrderByNode):
            return False
        if self.ordering_terms == other.ordering_terms:
            return True
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


@dataclass
class LimitNode(SqlAstNode):
    expr: List[ExpressionNode]

    def accept(self, visitor):
        return visitor.visit_limit(self)

    def __eq__(self, other):
        if not isinstance(other, LimitNode):
            return False
        if self.expr == other.expr:
            return True
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


@dataclass
class FromClauseNode(SqlAstNode):
    tables: List[TableOrSubqueryNode]
    join_clause: Optional[JoinClauseNode] = None

    def accept(self, visitor):
        return visitor.visit_from_clause(self)

    def __add__(self, other):
        if isinstance(other, TableOrSubqueryNode):
            return replace(self, tables=self.tables + [other])
        else:
            raise RuntimeError("Invalid operand type: {}".format(type(other)))

    def __eq__(self, other):
        if not isinstance(other, FromClauseNode):
            return False
        if set(self.tables) == set(other.tables) and self.join_clause == other.join_clause:
            return True
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


@dataclass
class WhereClauseNode(SqlAstNode):
    expr: ExpressionNode

    def accept(self, visitor):
        return visitor.visit_where_clause(self)

    def __eq__(self, other):
        if not isinstance(other, WhereClauseNode):
            return False
        ve = variable_extractor(self.expr)
        vo = variable_extractor(other.expr)
        if ve == vo:
            return True
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


@dataclass
class GroupClauseNode(SqlAstNode):
    exprs: List[ExpressionNode]
    having: Optional[ExpressionNode] = None
    rollup: bool = False

    def __add__(self, other):
        if isinstance(other, ExpressionNode):
            return replace(self, exprs=self.exprs + [other])
        else:
            raise RuntimeError("Invalid operand type: {}".format(type(other)))

    def accept(self, visitor):
        return visitor.visit_group_clause(self)

    def __eq__(self, other):
        if not isinstance(other, GroupClauseNode):
            return False
        if set(self.exprs) == set(other.exprs) and self.having == other.having:
            return True
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


@dataclass
# 2: the select
class SelectCoreNode(SqlAstNode):
    select_clause: SelectClauseNode
    from_clause: Optional[FromClauseNode] = None
    where_clause: Optional[WhereClauseNode] = None
    group_clause: Optional[GroupClauseNode] = None

    def accept(self, visitor):
        return visitor.visit_select_core(self)

    def __eq__(self, other):
        if not isinstance(other, SelectCoreNode):
            return False
        if self.select_clause == other.select_clause and \
                self.from_clause == other.from_clause and \
                self.where_clause == other.where_clause and \
                self.group_clause == other.group_clause:
            return True
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


@dataclass
class CommonTableExpressionNode(SqlAstNode):
    table_name: LiteralNode
    columns: List[ColumnNode]
    select_stmt: "SelectStatementNode"

    def accept(self, visitor):
        return visitor.visit_common_table_expression(self)

    def __add__(self, other):
        if isinstance(other, ColumnNode):
            return replace(self, columns=self.columns + [other])
        else:
            raise RuntimeError("Invalid operand type: {}".format(type(other)))

    def __eq__(self, other):
        if not isinstance(other, CommonTableExpressionNode):
            return False
        if self.table_name == other.table_name and \
                self.columns == other.columns and \
                self.select_stmt == other.select_stmt:
            return True
        else:
            return False

    def __hash__(self):
        return 1


@dataclass
class WithClauseNode(SqlAstNode):
    common_table_expr: List[CommonTableExpressionNode]

    def accept(self, visitor):
        return visitor.visit_with_clause(self)

    def __add__(self, other):
        if isinstance(other, CommonTableExpressionNode):
            return replace(self, common_table_expr=self.common_table_expr + [other])
        else:
            raise RuntimeError("Invalid operand type: {}".format(type(other)))

    def __hash__(self):
        return 1

    def __eq__(self, other):
        if not isinstance(other, WithClauseNode):
            return False
        if self.common_table_expr == other.common_table_expr:
            return True
        else:
            self.log_self()
            return False


@dataclass
# 1: all the sql statement
class SelectStatementNode(ExpressionNode):
    select_cores: List[SelectCoreNode]
    set_ops: List[TerminalNode]
    orderby: Optional[OrderByNode] = None
    limit: Optional[LimitNode] = None
    with_clause: Optional[WithClauseNode] = None

    def has_sub_expr(self):
        return True

    def add_core(self, set_op: TerminalNode, select_core: SelectCoreNode):
        return replace(self,
                       select_cores=self.select_cores + [select_core],
                       set_ops=self.set_ops + [set_op])

    def accept(self, visitor):
        return visitor.visit_select_statement(self)

    def __eq__(self, other):
        if not isinstance(other, SelectStatementNode):
            return False
        if set(self.select_cores) == set(other.select_cores) and set(self.set_ops) == set(other.set_ops) and \
                self.orderby == other.orderby and \
                self.with_clause == other.with_clause and \
                self.limit == other.limit:
            return True
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


@dataclass
class CastExpressionNode(ExpressionNode):
    expr: ExpressionNode
    type_name: TerminalNode  # all things that we don't know to use which func!

    def accept(self, visitor):
        return visitor.visit_cast_expression(self)

    def __eq__(self, other):
        if not isinstance(other, CastExpressionNode):
            return False
        if self.expr == other.expr and self.type_name == other.type_name:
            return True
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


@dataclass
class WindowDefinitionNode(SqlAstNode):
    cols: List[ResultColumnNode]
    orderby: Optional[OrderByNode] = None

    def accept(self, visitor):
        return visitor.visit_window_definition(self)

    def __add__(self, other):
        if isinstance(other, ResultColumnNode):
            return replace(self, cols=self.cols + [other])
        else:
            raise RuntimeError("Invalid operand type: {}".format(type(other)))

    def __eq__(self, other):
        if not isinstance(other, WindowDefinitionNode):
            return False
        if self.orderby == other.orderby and self.col == other.col:
            return True
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


@dataclass
class WindowExpressionNode(ExpressionNode):
    win_fun: TerminalNode
    win_fun_exprs: List[ExpressionNode]
    win_def: WindowDefinitionNode
    distinct: bool = False

    def accept(self, visitor):
        return visitor.visit_window_expression(self)

    def __eq__(self, other):
        if not isinstance(other, WindowExpressionNode):
            return False
        if self.win_fun == other.win_fun and self.win_def == other.win_fun:
            return True
        else:
            self.log_self()
            return False

    def __hash__(self):
        return 1


def variable_extractor(expr: ExpressionNode) -> Set[SqlAstNode]:
    if not isinstance(expr, BinOpExpressionNode):
        return set()
    else:
        if expr.op.value in {'and', 'or'}:
            return variable_extractor(expr.left).union(variable_extractor(expr.right)).union([expr.op])
        else:
            return {expr}
