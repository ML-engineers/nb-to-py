from nb_to_py.function import FunctionBuilder
from nb_to_py.cell import CellBuilder
from nb_to_py.refactoring import FunctionsUtils
from tests.models.example_functions import foo0, foo1, foo2
from tests import utils
from pytest_unordered import unordered
 

builder = FunctionBuilder()
sources =[
    utils.function_to_lines(foo0),
    utils.function_to_lines(foo1),
    utils.function_to_lines(foo2),
]
cell_builder = CellBuilder()
cells = [cell_builder.build({"cell_type": "code", "source": source}) for source in sources]
functions = [builder.build(cell, f'foo{i}') for i, cell in enumerate(cells)]
functions1 = functions[::-1].copy()

def test_verify_markdown_cell():
    broken_source = [
        "def myfunc(a: int, b:int):\n",
        "    import pippo\n",
        "    return a+b\n",
        "\n",
        "x=myfunc(ciao,2)\n",
    ]
    src_no_import, src_with_import = builder._get_body(broken_source)

    assert len(src_no_import) == len(broken_source) - 1
    assert src_with_import == ["import pippo\n"]


def test_create_dependency_dict():
    FunctionsUtils.update_function_output(functions)
    FunctionsUtils.filter_input_by_import_statements(functions)
    result = FunctionsUtils.create_dependency_dict(functions)
    assert result == {'foo0': [], 'foo1': [], 'foo2': unordered([('foo0', 'r1'),('foo1', 'r2')])}

    # reverse order -> different result
    FunctionsUtils.update_function_output(functions1)
    FunctionsUtils.filter_input_by_import_statements(functions1)
    result1 = FunctionsUtils.create_dependency_dict(functions1)
    assert result1 == {'foo0': [], 'foo1': [], 'foo2': []}

