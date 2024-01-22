from typing import TextIO, List, Tuple
import ast
from nb_to_py.cell import Cell
import ast
from typing import Iterator, Any
import re

from nb_to_py.visit import DeepNodeVisitor
from nb_to_py.function import Function


class FunctionsUtils:
    @staticmethod
    def update_function_output(functions: List[Function]):
        for i, f in enumerate(functions):
            f.output = set()
            for assigned in f.assigned:
                for j, f2 in enumerate(functions[i + 1 :]):
                    if assigned in f2.loaded:
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
            f.loaded = f.loaded.difference(imported)


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
