from src.taxonomy.cat.tag_collector import TagCollector
from src.taxonomy.cat.tag_collector_result import TagCollectorResult
from src.taxonomy.cat.tags.sql_tag import OrderedTag
from src.taxonomy.parse.node import JoinClauseNode


class JoinTables(OrderedTag):
    SingleJoin = 1
    TwoJoin = 2
    MultiJoin = 3

    @staticmethod
    class Collector(TagCollector):
        def visit_join_clause(self, node: JoinClauseNode):
            tags = super().visit_join_clause(node)
            if len(node.tables) == 2:
                return tags + TagCollectorResult(JoinTables.SingleJoin)
            else:
                return tags + TagCollectorResult(JoinTables.MultiJoin)
