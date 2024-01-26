from nb_to_py.converter import NotebookConverter
from nb_to_py.notebook import NotebookBuilder, FilterMarkdownType
from nb_to_py.refactoring import FunctionsUtils
from nb_to_py.writer import Writer
from nb_to_py.source import SourceBuilder

if __name__ == "__main__":
    builder = NotebookBuilder()
    notebook = builder.build(filepath="sample.ipynb")
    notebook.merge_markdown_cells()
    source = SourceBuilder.build(notebook)
    # print("EXCLUDE")
    # print(notebook.filtered_cells_by_markdown_exclude_all)
    # print("KEEP LAST")
    # print(notebook.filtered_cells_by_markdown_keep_last)

    # if __name__ == "__main__":
    #     builder = NotebookBuilder()
    #     notebook = builder.build(filepath="tests/unit/sample.ipynb")
    #     notebook.merge_markdown_cells()
    #     # %%
    #     builder = FunctionBuilder()
    #     functions = []
    #     for i, cell in enumerate(notebook.cells):
    #         functions.append(builder.build_function(cell, f"foo_{i}")

    functions = source.functions

    FunctionsUtils.update_function_output(functions)
    FunctionsUtils.filter_input_by_import_statements(functions)
    d = FunctionsUtils.create_dependency_dict(functions)
    writer = Writer("refactored_sample.py")

    for f in functions:
        writer.write_lines(f.src_with_import)
    writer.write_str("\n")
    for f in functions:
        if not f.only_comments:
            writer.write_function(f)
