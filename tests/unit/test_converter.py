from nb_to_py.converter import Notebook, FilterMarkdownType

filepath_sample = "tests/unit/sample.ipynb"


def test_notebook_building():
    notebook = Notebook(filepath_sample)

    assert notebook.filepath == filepath_sample
    assert isinstance(notebook.json, dict)
    assert isinstance(notebook.cells, list)


def test_filter_markdown_cells_exclude_all():
    nb = Notebook(filepath_sample)
    fm_type = FilterMarkdownType.ExcludeAll

    nb.filter_markdown_cells(filter_comments=fm_type)

    assert "# IMPORT" not in nb.cells[0].get("source")[0]
    assert "# DATASET" not in nb.cells[2].get("source")[0]


def test_filter_markdown_cells_keep_last():
    nb = Notebook(filepath_sample)
    fm_type = FilterMarkdownType.KeepLast

    nb.filter_markdown_cells(filter_comments=fm_type)

    assert "# CLASSIFICATION METRICS" in nb.cells[8].get("source")[0]


def test_filter_code_cells_by_marker():
    nb = Notebook(filepath_sample)

    nb.filter_code_cells_by_marker()

    assert "# IMPORT" in nb.cells[0].get("source")[0]
    assert "data = dataset.load" in nb.cells[2].get("source")[0]
