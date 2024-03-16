from typing import List
from nb_to_py.function import Function, FunctionBuilder
from nb_to_py.notebook import Notebook
from nb_to_py.notebook import FilterMarkdownType
from nb_to_py.cell import Cell


class Source:
    def __init__(self, functions: List[Function]):
        self.functions = functions


class SourceBuilder:
    def _get_notebook_cells(
        self, notebook: Notebook, filter_markdown_cells_type: FilterMarkdownType
    ) -> List[Cell]:
        if filter_markdown_cells_type == FilterMarkdownType.KeepLast:
            return notebook.filtered_cells_by_markdown_keep_last
        elif filter_markdown_cells_type == FilterMarkdownType.ExcludeAll:
            return notebook.filtered_cells_by_markdown_exclude_all
        else:
            return notebook.cells

    def build(
        self, notebook: Notebook, filter_markdown_cells_type: FilterMarkdownType
    ) -> Source:
        function_builder = FunctionBuilder()
        cells = self._get_notebook_cells(notebook, filter_markdown_cells_type)
        functions = [
            function_builder.build(cell, f"foo_{i}") for i, cell in enumerate(cells)
        ]
        return Source(functions)
