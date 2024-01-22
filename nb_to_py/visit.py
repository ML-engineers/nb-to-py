from typing import Any, List
import ast


class DeepNodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.visited_nodes = []

    def generic_visit(self, node):
        self.visited_nodes.append(node)
        super().generic_visit(node)

    def _generic_visit_append_after(self, node):
        super().generic_visit(node)
        self.visited_nodes.append(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Any:
        self._generic_visit_append_after(node)

    def visit_Assign(self, node: ast.Assign) -> Any:
        self._generic_visit_append_after(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> Any:
        self._generic_visit_append_after(node)


def get_source_tree(source: List[str]) -> ast.Module:
    return ast.parse("".join(source))


def get_nodes_from_tree(tree: ast.Module, visitor: DeepNodeVisitor) -> List:
    visitor.visit(tree)
    return visitor.visited_nodes
