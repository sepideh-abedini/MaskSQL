from enum import Enum


class SqlTag(Enum):
    def __ge__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.value == other.value

    def __str__(self):
        return self.name


class OrderedTag(SqlTag):
    def __ge__(self, other):
        """t1 >= t2 ==> t1 is at least as hard as t2"""
        if not isinstance(other, self.__class__):
            return False
        return self.value >= other.value
