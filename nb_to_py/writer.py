from nb_to_py.refactoring import Function
from typing import TextIO, List


class Writer:
    def __init__(self, output_filepath: str):
        self.output_file = open(output_filepath, "w")

    def _source_generator(self, function: Function, indent_body: int = 1):
        indent_str = "\t" * indent_body
        input = ", ".join(function.loaded)
        output = ", ".join(function.output)
        body = indent_str + indent_str.join(function.body)
        source = f"def {function.name}({input}):\n{body}"
        source += f"\n{indent_str}return {output}\n" if output else ""
        source += "\n"
        return source

    def write_function(self, function: Function):
        self.output_file.write(self._source_generator(function))

    def write_lines(self, lines: List[str], indent: int = 0):
        indent_str = "\t" * indent
        self.output_file.write(indent_str + indent_str.join(lines))

    def write_str(self, source: str):
        self.output_file.write(source)
