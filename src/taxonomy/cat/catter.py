from src.cat.categorizer import Categorizer
from src.cat.tag_extractor import TagExtractor
from src.parse.parser import SqlParser

from loguru import logger


class Catter:
    parser = SqlParser()
    tag_extractor = TagExtractor()
    categorizer = Categorizer()

    def get_category(self, sql: str):
        try:
            ast = self.parser.parse(sql)
            tags = self.tag_extractor.extract_tags(ast)
            return self.categorizer.get_category(tags.tag_set)
        except Exception as e:
            logger.debug(e)
            return None

    def get_sub_category(self, sql: str):
        ast = self.parser.parse(sql)
        tags = self.tag_extractor.extract_tags(ast)
        return self.categorizer.get_sub_category(tags.tag_set)

    def categorize(self, sql: str):
        return self.get_category(sql), self.get_sub_category(sql)
