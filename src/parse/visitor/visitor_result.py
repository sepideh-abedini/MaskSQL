from abc import ABC, abstractmethod


class MergeableVisitorResult(ABC):
    """Contains the result of visiting an AstNode.
       The result of a node children can be merged to compose
       the result of visiting parent node."""

    def __add__(self, other):
        return self.merge(other)

    @abstractmethod
    def merge(self, other):
        pass
