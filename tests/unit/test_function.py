from nb_to_py.function import FunctionBuilder


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
