from nb_to_py.converter import NotebookConverter
from nb_to_py.notebook import NotebookBuilder, FilterMarkdownType
import ast
from nb_to_py.refactoring import FunctionBuilder, FunctionOutputCalculator


if __name__ == "__main__":
    builder = NotebookBuilder()
    notebook = builder.build_notebook(filepath="tests/unit/sample.ipynb")
    # %%
    builder = FunctionBuilder()
    functions = []
    for cell in notebook.cells:
        functions.append(builder.build_function(cell))

    FunctionOutputCalculator.update_function_output(functions)

    for f in functions:
        print(f"INPUT: {f.input}")
        print(f"ASSIGNED: {f.assigned}")
        print(f"OUTPUT: {f.output}")
        print("----")
