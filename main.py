from nb_to_py.converter import NotebookConverter
from nb_to_py.notebook import NotebookBuilder, FilterMarkdownType
import ast
from nb_to_py.refactoring import FunctionBuilder, FunctionsUtils
from nb_to_py.writer import Writer


if __name__ == "__main__":
    builder = NotebookBuilder()
    notebook = builder.build_notebook(filepath="tests/unit/sample.ipynb")
    notebook.merge_markdown_cells()
    # %%
    builder = FunctionBuilder()
    functions = []
    for i, cell in enumerate(notebook.cells):
        functions.append(builder.build_function(cell, f"foo_{i}"))

    FunctionsUtils.update_function_output(functions)
    FunctionsUtils.filter_input_by_import_statements(functions)
    writer = Writer("refactored_sample.py")

    for f in functions:
        writer.write_lines(f.imported_body)
    writer.write_str("\n")
    for f in functions:
        if not f.only_comments:
            writer.write_function(f)
