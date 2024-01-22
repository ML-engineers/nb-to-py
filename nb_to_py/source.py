from typing import List
from nb_to_py.function import Function, FunctionBuilder
from nb_to_py.notebook import Notebook


class Source:
    def __init__(self, functions: List[Function]):
        self.functions = functions


class SourceBuilder:
    
    @staticmethod
    def build(notebook: Notebook) -> Source:
        function_builder = FunctionBuilder()
        cells = notebook.cells
        # TODO: filter
        functions = [function_builder.build(cell, f"foo_{i}") for i, cell in enumerate(cells)]
        return Source(functions)
