from typing import List, Optional

from graphviz import Digraph

from src.parse.visitor.visitor_result import MergeableVisitorResult


class DiagramTreeNode(MergeableVisitorResult):
    name: str
    parent: Optional['DiagramTreeNode']
    children: List['DiagramTreeNode']
    shape: str

    def __init__(self, name: str, shape: str = 'box'):
        self.name = name
        self.parent = None
        self.children = []
        self.shape = shape

    def merge(self, other):
        return self.add_child(other)

    def add_child(self, child: 'DiagramTreeNode'):
        if child is not None:
            child.parent = self
            self.children.append(child)
        return self

    def add_to_graph(self, graph: Digraph):
        """Recursively add this node and its children to the graph"""
        graph.node(self.id(), self.name, shape=self.shape)
        if self.parent:
            graph.edge(self.parent.id(), self.id())
        for child in self.children:
            child.add_to_graph(graph)

    def get_num_nodes(self) -> int:
        size = 1
        for c in self.children:
            size += c.get_num_nodes()
        return size

    def get_height(self) -> int:
        if len(self.children) == 0:
            return 1
        return max([c.get_height() + 1 for c in self.children])

    def id(self):
        return str(id(self))
