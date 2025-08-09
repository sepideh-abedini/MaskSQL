from src.cat.tag_collector import TagCollector
from src.cat.tag_collector_result import TagCollectorResult
from src.cat.tags.sql_tag import OrderedTag
from src.parse.node import GroupClauseNode


class GroupType(OrderedTag):
    UnconditionalGroup = 1
    ConditionalGroup = 2

    @staticmethod
    class Collector(TagCollector):
        def visit_group_clause(self, node: GroupClauseNode):
            tags = super().visit_group_clause(node)
            if node.having:
                return tags + TagCollectorResult(GroupType.ConditionalGroup)
            else:
                return tags + TagCollectorResult(GroupType.UnconditionalGroup)
