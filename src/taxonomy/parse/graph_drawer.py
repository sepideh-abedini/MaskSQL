import graphviz

from src.taxonomy.parse.node import SqlAstNode
from src.taxonomy.parse.visitor.tree_extractor import AstDiagramTreeExtractor


def draw_graph(ast: SqlAstNode, out_path: str):
    visitor = AstDiagramTreeExtractor()
    root = ast.accept(visitor)
    graph = graphviz.Digraph(comment=ast.__class__.__name__)
    root.add_to_graph(graph)
    graph.render(out_path, format='png', cleanup=True)
