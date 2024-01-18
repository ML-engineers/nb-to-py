from typing import TextIO, List, Tuple
import ast
from nb_to_py.cell import Cell
import ast


class My_Visitor(ast.NodeVisitor):
    visited_nodes=[]

    def generic_visit(self, node):
        self.visited_nodes.append(node)
        ast.NodeVisitor.generic_visit(self, node)


class Function:
    def __init__(self, body: str, input: Tuple[str], output: Tuple[str]):
        self.input = input
        self.output = output
        self.body = body


class FunctionBuilder:
    def _get_source_tree(self, source) -> ast.Module:
        return ast.parse(source)

    def _extract_variables(self, tree: ast.Module) -> Tuple[set[str], set[str]]:
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

        x = My_Visitor()
        x.visit(tree)

        for node in x.visited_nodes:
            if isinstance(node, ast.Assign):
                assigned.update(get_variables_from_node(node))
            elif (
                isinstance(node, ast.Name)
                and isinstance(node.ctx, ast.Load)
                and node.id not in assigned
            ):
                input.add(node.id)
        return input, assigned

    def build_function(self, cell: Cell):
        tree = self._get_source_tree(cell.source)
        input, assigned = self._extract_variables(tree)
        return Function("", input, assigned)


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
