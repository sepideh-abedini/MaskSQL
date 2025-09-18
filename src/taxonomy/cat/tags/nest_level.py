from src.taxonomy.cat.tag_collector import TagCollector
from src.taxonomy.cat.tag_collector_result import TagCollectorResult
from src.taxonomy.cat.tags.sql_tag import SqlTag
from src.taxonomy.cat.tags.structure import StructureType
from src.taxonomy.parse.node import SelectStatementNode


class NestLevel(SqlTag):
    Zero = 0
    One = 1
    Two = 2
    Many = 3

    @staticmethod
    class Collector(TagCollector):

        def __init__(self):
            super().__init__()
            self.cur_level = 0
            self.max_level = 0

        def visit_select_statement(self, node: SelectStatementNode):
            self.cur_level += 1
            if self.cur_level > self.max_level:
                self.max_level = self.cur_level
            tags = super().visit_select_statement(node)
            max_level = self.max_level
            match max_level:
                case 1:
                    tags += TagCollectorResult(NestLevel.Zero)
                case 2:
                    tags += TagCollectorResult(NestLevel.One)
                case 3:
                    tags += TagCollectorResult(NestLevel.Two)
                case max_level if max_level > 3:
                    tags += TagCollectorResult(NestLevel.Many)
            self.cur_level -= 1
            return tags
