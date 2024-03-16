from nb_to_py.refactoring import Function
from typing import TextIO, List


class Writer:
    def __init__(self, output_filepath: str):
        self.output_file = open(output_filepath, "w")
        self._function_calls = []

    def _source_generator(self, function: Function, indent_body: int = 1):
        indent_str = "\t" * indent_body
        input = ", ".join(function.loaded)
        outputs = ", ".join(function.outputs)
        body = indent_str + indent_str.join(function.body)
        source = f"def {function.name}({input}):\n{body}"
        source += f"\n{indent_str}return {outputs}\n" if outputs else ""
        source += "\n"
        return source

    def _call_generator(self, function: Function):
        input = ", ".join(function.loaded)
        source = f"{function.name}({input})\n"
        if function.outputs:
            outputs = ", ".join(function.outputs)
            source = f"{outputs} = {source}"
        self._function_calls.append(source)

    def write_function(self, function: Function):
        self.output_file.write(self._source_generator(function))
        self._call_generator(function)

    def write_lines(self, lines: List[str], indent: int = 0):
        indent_str = "\t" * indent
        self.output_file.write(indent_str + indent_str.join(lines))

    def write_str(self, source: str):
        self.output_file.write(source)

    def write_function_calls(self, allow_empty_return: bool = False):
        calls = (
            [call for call in self._function_calls if "=" in call]
            if not allow_empty_return
            else self._function_calls
        )
        for call in calls:
            self.output_file.write(call)
