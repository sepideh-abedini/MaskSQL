from src.taxonomy.cat.tag_collector import TagCollector
from src.taxonomy.cat.tag_collector_result import TagCollectorResult
from src.taxonomy.cat.tags.sql_tag import OrderedTag
from src.taxonomy.parse.node import JoinClauseNode


class JoinConditions(OrderedTag):
    UnconditionalJoin = 1
    ConditionalJoin = 2

    @staticmethod
    class Collector(TagCollector):
        def visit_join_clause(self, node: JoinClauseNode):
            tags = super().visit_join_clause(node)
            if any(con is not None for con in node.constraints):
                return tags + TagCollectorResult(JoinConditions.ConditionalJoin)
            else:
                return tags + TagCollectorResult(JoinConditions.UnconditionalJoin)
