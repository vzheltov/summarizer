import os
import sys

import pandas as pd
import pytest


from summarizer import Summarizer


def test_numeric_column():
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5]})
    out = Summarizer(df).analyze()
    assert out.loc["x", "kind"] == "numeric"
    assert out.loc["x", "min"] == 1.0
    assert out.loc["x", "max"] == 5.0
    assert out.loc["x", "mean"] == 3.0


def test_categorical_column():
    df = pd.DataFrame({"c": ["a", "b", "a", "a"]})
    out = Summarizer(df).analyze()
    assert out.loc["c", "kind"] == "categorical"
    assert out.loc["c", "mode"] == "a"
    assert out.loc["c", "distinct"] == 2


def test_boolean_column():
    df = pd.DataFrame({"b": [True, False, True, True]})
    out = Summarizer(df).analyze()
    assert out.loc["b", "kind"] == "boolean"
    assert out.loc["b", "true_pct"] == 75.0
    assert out.loc["b", "false_pct"] == 25.0


def test_report_markdown():
    df = pd.DataFrame({"x": [1, 2, 3]})
    md = Summarizer(df).report("markdown")
    assert "x" in md


def test_report_html():
    df = pd.DataFrame({"x": [1, 2, 3]})
    html = Summarizer(df).report("html")
    assert "<table" in html


def test_xlsx_requires_filename():
    df = pd.DataFrame({"x": [1, 2, 3]})
    with pytest.raises(ValueError):
        Summarizer(df).report("xlsx")


def test_summarizer_rejects_non_dataframe():
    with pytest.raises(TypeError):
        Summarizer([1, 2, 3])
