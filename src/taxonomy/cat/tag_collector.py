from src.taxonomy.cat.tag_collector_result import TagCollectorResult
from src.taxonomy.parse.node import *
from src.taxonomy.parse.visitor.collector_visitor import CollectorVisitor


class TagCollector(CollectorVisitor):
    def __init__(self):
        super().__init__(TagCollectorResult)


class TableCountCollector(TagCollector):
    def __init__(self):
        super().__init__()
        self.uniq_table_names = set()

    def visit_from_clause(self, node: FromClauseNode):
        for table in node.tables:
            if table.table_name:
                self.uniq_table_names.add(table.table_name)
