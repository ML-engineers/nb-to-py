from enum import Enum
from typing import List


class CellType(Enum):
    Code = "code"
    Markdown = "markdown"


class Cell:
    KEEP_MARKERS = ["# KEEP"]

    def __init__(self, cell_type: CellType, is_marked: bool, source: str):
        self.cell_type = cell_type
        self.is_marked = is_marked
        self.source = source


class CellBuilder:
    def _build_cell_type(self, cell_type: str) -> CellType:
        return CellType(cell_type)

    def _build_is_marked(self, source: List[str], cell_type: CellType) -> bool:
        return (
            cell_type == CellType.Code
            and source is not None
            and len(source) > 0
            and any(marker in source[0] for marker in Cell.KEEP_MARKERS)
        )

    def _build_source(self, source: List[str], is_marked: bool) -> str:
        if not is_marked:
            return "".join(source)
        elif len(source) > 1:
            return "".join(source[1:])
        else:
            return ""

    def build_cell(self, cell_dict: dict):
        cell_type = self._build_cell_type(cell_dict.get("cell_type"))
        is_marked = self._build_is_marked(cell_dict.get("source"), cell_type)
        source = self._build_source(cell_dict.get("source"), is_marked)
        return Cell(cell_type, is_marked, source)
