from nb_to_py.converter import NotebookConverter
from nb_to_py.notebook import NotebookBuilder, FilterMarkdownType
import ast
from nb_to_py.refactoring import (
    FunctionBuilder,
    FunctionOutputCalculator,
    FunctionWriter,
)


if __name__ == "__main__":
    builder = NotebookBuilder()
    notebook = builder.build_notebook(filepath="tests/unit/sample.ipynb")
    # %%
    builder = FunctionBuilder()
    functions = []
    for i, cell in enumerate(notebook.cells):
        functions.append(builder.build_function(cell, f"foo_{i}"))

    FunctionOutputCalculator.update_function_output(functions)

    open("refactored_sample.py", "w")
    for f in functions:
        FunctionWriter().write(f, open("refactored_sample.py", "a"))
