from nb_to_py.converter import NotebookConverter
from nb_to_py.notebook import NotebookBuilder, FilterMarkdownType
import ast
from nb_to_py.refactoring import FunctionBuilder





if __name__ == "__main__":
    builder = NotebookBuilder()
    notebook = builder.build_notebook(filepath="tests/unit/sample.ipynb")
    # %%
    builder = FunctionBuilder()
    f = builder.build_function(notebook.cells[0])
    print("input:")
    print(f.input)
    print("assigned:")
    print(f.assigned)
