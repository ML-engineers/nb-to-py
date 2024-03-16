from typing import List, Tuple
from nb_to_py.cell import Cell
import ast
import re
from nb_to_py import visit
from nb_to_py.cell import CellType


class Function:
    def __init__(
        self,
        body: List[str],
        loaded: set,
        assigned: set,
        imported: set,
        src_with_import: List[str],
        name: str,
        only_comments: bool,
    ):
        self.body = body
        self.loaded = loaded
        self.assigned = assigned
        self.imported = imported
        self.src_with_import = src_with_import
        self.name = name
        self.outputs = None
        self.only_comments = only_comments


class FunctionBuilder:
    IMPORT_PATTERN = re.compile(
        r"^\s*import\s+[\w,]+\s*$|^\s*from\s+[\w.]+\s+import\s+[\w,]+\s*$"
    )

    def _has_body_only_comments(self, body: List[str]):
        return all([line.strip().startswith(("#", '"""')) for line in body])

    def _add_comment_markdown_cell(self, source: List[str]) -> List[str]:
        return [line if line.startswith("#") else f"# {line}" for line in source]

    def _build_source(self, cell: Cell) -> List[str]:
        if cell.cell_type == CellType.Markdown:
            return self._add_comment_markdown_cell(cell.source)
        return cell.source

    def _get_body(self, source: List[str]) -> Tuple[List[str], List[str]]:
        src_no_import = []
        src_with_import = []
        for line in source:
            if re.match(self.IMPORT_PATTERN, line):
                src_with_import.append(line.lstrip())
            else:
                src_no_import.append(line)
        return src_no_import, src_with_import

    def _get_imported(self, nodes: list) -> set[str]:
        imported = set()
        for node in nodes:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for n in node.names:
                    imported.add(n.asname or n.name)
        return imported

    def _extract_variables(self, nodes: list) -> Tuple[set[str], set[str]]:
        def get_variables_from_node(node) -> set[str]:
            variables = set()
            for target in node.targets:
                if isinstance(target, ast.Name):
                    variables.add(target.id)
                elif isinstance(target, ast.Tuple):
                    for elt in target.elts:
                        variables.add(elt.id)
            return variables

        assigned = set()
        loaded = set()

        for node in nodes:
            if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                assigned.update(get_variables_from_node(node))
            elif (
                isinstance(node, ast.Name)
                and isinstance(node.ctx, ast.Load)
                and node.id not in assigned
            ):
                loaded.add(node.id)
        return loaded, assigned

    def build(self, cell: Cell, name: str):
        source = self._build_source(cell)
        tree = visit.get_source_tree(source)
        visitor = visit.DeepNodeVisitor()
        nodes = visit.get_nodes_from_tree(tree, visitor)
        loaded, assigned = self._extract_variables(nodes)
        imported = self._get_imported(nodes)
        src_no_import, src_with_import = self._get_body(source)
        only_comments = self._has_body_only_comments(src_no_import)
        return Function(
            src_no_import,
            loaded,
            assigned,
            imported,
            src_with_import,
            name,
            only_comments,
        )
