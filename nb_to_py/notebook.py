from enum import Enum
from typing import List, Optional
from nb_to_py.cell import Cell, CellType, CellBuilder
import json


class FilterMarkdownType(Enum):
    KeepLast = "keep_last"
    ExcludeAll = "exclude_all"


class Notebook:
    def __init__(self, filepath: str, cells: List[Cell]):
        self.filepath = filepath
        self.cells = cells

    @staticmethod
    def _exclude_all_mardown_cells(cells: List[Cell]) -> List[Cell]:
        return [cell for cell in cells if cell.cell_type != CellType.Markdown]


    @staticmethod
    def _keep_last_markdown_cell(cells: List[Cell]) -> List[Cell]:
        new_cells = []
        previous_cell = None
        for cell in cells:
            if (
                previous_cell is not None
                and previous_cell.cell_type == CellType.Markdown
                and cell.cell_type == CellType.Code
            ):
                new_cells.append(previous_cell)
            if cell.cell_type != CellType.Markdown:
                new_cells.append(cell)

            previous_cell = cell
        return new_cells

    @property
    def filtered_cells_by_markdown_keep_last(self):
        return self._keep_last_markdown_cell(self.cells)

    @property
    def filtered_cells_by_markdown_exclude_all(self):
        return self._exclude_all_mardown_cells(self.cells)


    def filter_markdown_cells(self, filter_markdown_cells_type: FilterMarkdownType):
        if filter_markdown_cells_type == FilterMarkdownType.KeepLast:
            self.cells = self._keep_last_markdown_cell()
        elif filter_markdown_cells_type == FilterMarkdownType.ExcludeAll:
            self.cells = self._exclude_all_mardown_cells()

    def filter_code_cells_by_marker(self):
        self.cells = [
            cell
            for cell in self.cells
            if cell.cell_type != CellType.Code
            or (cell.cell_type == CellType.Code and cell.is_marked)
        ]

    def merge_markdown_cells(self):
        source = []
        cells = []
        for cell in self.cells:
            if cell.cell_type == CellType.Markdown:
                source.extend(cell.source)
            elif cell.cell_type == CellType.Code:
                cell.source = source + cell.source
                cells.append(cell)
                source = []
        self.cells = cells


class NotebookBuilder:
    def _read_json(self, filepath: str) -> dict:
        with open(filepath, "r") as f:
            nb = json.load(f)
        return nb

    def _build_cells(self, builder: CellBuilder, nb_cells: List[dict]) -> List[Cell]:
        return [builder.build_cell(cell) for cell in nb_cells]

    def build_notebook(
        self,
        filepath: str,
    ):
        nb = self._read_json(filepath)
        builder = CellBuilder()
        cells = self._build_cells(builder, nb.get("cells"))
        return Notebook(filepath, cells)
