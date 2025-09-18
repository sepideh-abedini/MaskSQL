from typing import Any

from src.taxonomy.parse.node import TerminalNode, SelectStatementNode, \
    JoinClauseNode, SqlAstNode
from src.taxonomy.parse.tree_node import DiagramTreeNode
from src.taxonomy.parse.visitor.collector_visitor import CollectorVisitor
from src.util.str_utils import split_pascal


class AstDiagramTreeExtractor(CollectorVisitor):
    def __init__(self):
        super().__init__(DiagramTreeNode)

    def get_new_result_instance(self, attr: Any):
        if attr:
            if isinstance(attr, SqlAstNode):
                name = attr.__class__.__name__
                name = name.replace("Node", "")
                name = split_pascal(name)
                root = DiagramTreeNode(name)
                return root
            else:
                return DiagramTreeNode(str(attr))
        else:
            return None

    def get_join_attrs(self, node: JoinClauseNode):
        """Returns join attributes as a list with the pattern: (table [op] [constraint])*"""
        attrs = []
        if len(node.tables) > 0:
            attrs.append(node.tables[0])
            for (table, op, constraint) in zip(node.tables[1:], node.ops, node.constraints):
                attrs.append(op)
                attrs.append(table)
                if constraint:
                    attrs.append(constraint)
        return attrs

    def get_select_stmt_attrs(self, node: SelectStatementNode):
        """Returns select attributes as a list with the pattern: select_core (op select_core)*"""
        attrs = []
        if len(node.select_cores) > 0:
            attrs.append(node.select_cores[0])
            for (core, op) in zip(node.select_cores[1:], node.set_ops):
                attrs.append(op)
                attrs.append(core)
        if node.orderby:
            attrs.append(node.orderby)
        if node.limit:
            attrs.append(node.limit)
        return attrs

    def get_attrs(self, node: SqlAstNode):
        if isinstance(node, JoinClauseNode):
            return self.get_join_attrs(node)
        elif isinstance(node, SelectStatementNode):
            return self.get_select_stmt_attrs(node)
        else:
            return super().get_attrs(node)

    def visit_terminal(self, node: TerminalNode):
        return DiagramTreeNode("{}:{}".format(node.name, node.value), 'ellipse')
