from typing import TextIO, List, Tuple
import ast
from nb_to_py.cell import Cell
import ast
from typing import Iterator


class DeepVisitor(ast.NodeVisitor):
    def __init__(self):
        self.visited_nodes = []

    def visit(self, node):
        """Visit a node."""
        self.visited_nodes.append(node)
        super().visit(node)


class Function:
    def __init__(self, body: str, input: set, assigned: set, name: str):
        self.input = input
        self.assigned = assigned
        self.body = body
        self.name = name
        self.output = None


class FunctionBuilder:
    def _get_source_tree(self, source: str) -> ast.Module:
        return ast.parse(source)

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
        return Function(cell.source, input, assigned, name)


class FunctionOutputCalculator:
    @staticmethod
    def update_function_output(functions: List[Function]):
        for i, f in enumerate(functions):
            f.output = set()
            for assigned in f.assigned:
                for j, f2 in enumerate(functions[i + 1 :]):
                    if assigned in f2.input:
                        f.output.add(assigned)
                        break


class FunctionWriter:
    def _source_generator(self, function: Function):
        input = ",".join(function.input)
        output = ",".join(function.output)
        body = "\t" + function.body.replace("\n", "\n\t")
        source = f"def {function.name}({input}):\n{body}\n"
        source += f"\treturn {output}\n" if output else ""
        source +="\n"
        return source

    def write(self, function: Function, output_file: TextIO):
        output_file.write(self._source_generator(function))


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
