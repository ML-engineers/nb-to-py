from typing import TextIO, List, Tuple
import ast
from nb_to_py.cell import Cell
import ast
from typing import Iterator, Any
import re


class Function:
    def __init__(
        self,
        body: List[str],
        input: set,
        assigned: set,
        imported: set,
        imported_body: List[str],
        name: str,
        only_comments: bool,
    ):
        self.body = body
        self.input = input
        self.assigned = assigned
        self.imported = imported
        self.imported_body = imported_body
        self.name = name
        self.output = None
        self.only_comments = only_comments


class Source:
    def __init__(self, functions: List[Function]):
        self.functions = functions

    pass

    def set_input(self):
        pass


class SourceBuilder:
    pass


class FunctionBuilder:
    IMPORT_PATTERN = re.compile(
        r"^\s*import\s+[\w,]+\s*$|^\s*from\s+[\w.]+\s+import\s+[\w,]+\s*$"
    )

    def _has_body_only_comments(self, body: List[str]):
        for line in body:
            if not line.strip().startswith(("#", '"""')):
                return False
        return True

    def _get_body(self, source: List[str]) -> Tuple[List[str], List[str]]:
        body = []
        imported_body = []
        for line in source:
            if re.match(self.IMPORT_PATTERN, line):
                imported_body.append(line)
            else:
                body.append(line)
        return body, imported_body

    def _get_imported(self, nodes: list) -> set[str]:
        imported = set()
        for node in nodes:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for n in node.names:
                    imported.add(n.asname or n.name)
        return imported

    def _get_source_tree(self, source: List[str]) -> ast.Module:
        return ast.parse("".join(source))

    def _get_nodes_from_tree(self, tree: ast.Module) -> list:
        visitor = DeepVisitor()
        visitor.visit(tree)
        return visitor.visited_nodes

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
        input = set()

        for node in nodes:
            if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                assigned.update(get_variables_from_node(node))
            elif (
                isinstance(node, ast.Name)
                and isinstance(node.ctx, ast.Load)
                and node.id not in assigned
            ):
                input.add(node.id)
        return input, assigned

    def build_function(self, cell: Cell, name: str):
        tree = self._get_source_tree(cell.source)
        nodes = self._get_nodes_from_tree(tree)
        input, assigned = self._extract_variables(nodes)
        imported = self._get_imported(nodes)
        body, imported_body = self._get_body(cell.source)
        only_comments = self._has_body_only_comments(body)
        return Function(
            body, input, assigned, imported, imported_body, name, only_comments
        )


class FunctionsUtils:
    @staticmethod
    def update_function_output(functions: List[Function]):
        for i, f in enumerate(functions):
            f.output = set()
            for assigned in f.assigned:
                for j, f2 in enumerate(functions[i + 1 :]):
                    if assigned in f2.input:
                        f.output.add(assigned)
                        break

    @staticmethod
    def _get_all_imported(functions: List[Function]):
        imported = set()
        for f in functions:
            imported.update(f.imported)
        return imported

    @staticmethod
    def filter_input_by_import_statements(functions: List[Function]):
        imported = FunctionsUtils._get_all_imported(functions)
        for f in functions:
            f.input = f.input.difference(imported)


class RefactorCellAdapter:
    def __init__(self, cell: Cell):
        self.cell = cell


class RefactorHandler:
    def __init__(self, input_file: TextIO, output_file: TextIO):
        self.input_file = input_file
        self.output_file = output_file
        self.imported = None
        self.cells_variables = None

    def refactor(self, import_tree: ast.Module, cells_trees: List[ast.Module]):
        self.imported = self._get_import(import_tree)
        cells_variables = []
        for tree in cells_trees:
            cells_variables.append(self._get_variables(tree, self.imported))
        self.cells_variables = cells_variables

    @staticmethod
    def _get_import(tree: ast.Module):
        imp = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for n in node.names:
                    imp.add(n.asname or n.name)
        return imp
