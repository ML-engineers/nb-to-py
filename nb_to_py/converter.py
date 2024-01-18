from typing import TextIO
from nb_to_py.notebook import Notebook


class NotebookConverter:
    @staticmethod
    def convert(
        notebook: Notebook,
        output_file: TextIO,
    ):
        output_file.write("\n\n".join([cell.source for cell in notebook.cells]))
