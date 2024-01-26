from nb_to_py.function import FunctionBuilder
from nb_to_py.cell import CellBuilder
from nb_to_py.refactoring import FunctionsUtils

builder = FunctionBuilder()


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
    sources =[
        ['def foo0(p1, p2):\n', '    r1 = p1+p2\n', '    return r1'],
        ['def foo1():\n', '    r2 = r3 = 0\n', '    return r2, r3'],
        ['def foo2(r1, r2):\n', '    r4=r1+r2\n', '    return r4'],
    ]
    cell_builder = CellBuilder()
    cells = [cell_builder.build_cell({"cell_type": "code", "source": source}) for source in sources]
    functions = [builder.build(cell, f'foo{i}') for i, cell in enumerate(cells)]
    FunctionsUtils.update_function_output(functions)
    FunctionsUtils.filter_input_by_import_statements(functions)
    d = FunctionsUtils.create_dependency_dict(functions)
    assert d == {'foo0': [], 'foo1': [], 'foo2': [('foo1', 'r2'), ('foo0', 'r1')]}
