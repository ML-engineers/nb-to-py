from nb_to_py.cell import CellBuilder


builder = CellBuilder()


def test_verify_markdown_cell():
    source = ["# Markdown title", "markdown with no leading '#'"]
    result = builder._verify_markdown_cell(source)

    assert len(result) == len(source)
    assert all([line.startswith("#") for line in result])
