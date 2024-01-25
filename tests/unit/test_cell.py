from nb_to_py.cell import CellBuilder


builder = CellBuilder()


def test_verify_markdown_cell():
    broken_source = ["# Markdown title", "markdown with no leading '#'"]
    result = builder._verify_markdown_cell(broken_source)
    assert len(result) == len(broken_source)
    assert all([line.startswith("#") for line in result])

    source = ["# Markdown title", "## Markdown title"]
    result2 = builder._verify_markdown_cell(source)
    assert source == result2
