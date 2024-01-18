from nb_to_py.converter import NotebookConverter
from nb_to_py.notebook import NotebookBuilder, FilterMarkdownType
import ast

if __name__ == "__main__":
    builder = NotebookBuilder()
    notebook = builder.build_notebook(
        filepath="tests/unit/sample.ipynb"
    )
    # %%
    tree = ast.parse(notebook.cells[0].source)

    def get_import(tree):
        imp = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for n in node.names:
                    imp.add(n.asname or n.name)
        return imp


    def get_variables(tree):
        def get_variables_from_node(node):
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
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                assigned.update(get_variables_from_node(node))
            elif isinstance(node, ast.Name) and isinstance(node.ctx,
                                                           ast.Load) and node.id not in assigned:
                input.add(node.id)
        return input, assigned

    # %%
    variables = []
    for cell in notebook.cells:
        tree = ast.parse(cell.source)
        variables.append(get_variables(tree))
    # %%
    print(variables)




    builder = NotebookBuilder()
    notebook = builder.build_notebook(
        filepath="tests/unit/sample.ipynb",
    )
    #notebook.filter_code_cells_by_marker()
    #notebook.filter_markdown_cells(FilterMarkdownType.KeepLast)
    with open("provaaa.py", "w") as f:
        NotebookConverter.convert(notebook,f)
