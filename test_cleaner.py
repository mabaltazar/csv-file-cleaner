"""
csv_cleaner/test_cleaner.py

Unit tests for cleaner.py using pytest.
Run with: pytest test_cleaner.py -v
"""

import pytest
from pathlib import Path
from cleaner import normalize_header, is_empty_row, clean_row, clean_csv, load_csv, save_csv


# ── normalize_header ──────────────────────────────────────────────────────────

def test_normalize_header_strips_spaces():
    assert normalize_header("  First Name  ") == "first_name"

def test_normalize_header_lowercases():
    assert normalize_header("EMAIL") == "email"

def test_normalize_header_replaces_spaces_with_underscores():
    assert normalize_header("Phone Number") == "phone_number"

def test_normalize_header_already_clean():
    assert normalize_header("age") == "age"


# ── is_empty_row ──────────────────────────────────────────────────────────────

def test_is_empty_row_all_empty():
    assert is_empty_row({"name": "", "email": "  "}) is True

def test_is_empty_row_has_data():
    assert is_empty_row({"name": "Alice", "email": ""}) is False

def test_is_empty_row_all_filled():
    assert is_empty_row({"name": "Bob", "email": "bob@example.com"}) is False


# ── clean_row ─────────────────────────────────────────────────────────────────

def test_clean_row_strips_values():
    row = {"name": "  Alice  ", "email": " alice@example.com "}
    assert clean_row(row) == {"name": "Alice", "email": "alice@example.com"}

def test_clean_row_empty_values_stay_empty():
    row = {"name": "", "email": "   "}
    assert clean_row(row) == {"name": "", "email": ""}


# ── clean_csv ─────────────────────────────────────────────────────────────────

def test_clean_csv_removes_empty_rows():
    rows = [
        {"name": "Alice", "email": "alice@example.com"},
        {"name": "",      "email": ""},
        {"name": "Bob",   "email": "bob@example.com"},
    ]
    result = clean_csv(rows)
    assert len(result) == 2

def test_clean_csv_removes_duplicates():
    rows = [
        {"name": "Alice", "email": "alice@example.com"},
        {"name": "Alice", "email": "alice@example.com"},
        {"name": "Bob",   "email": "bob@example.com"},
    ]
    result = clean_csv(rows)
    assert len(result) == 2

def test_clean_csv_normalizes_headers():
    rows = [{"First Name": "Alice", "Email Address": "alice@example.com"}]
    result = clean_csv(rows)
    assert "first_name" in result[0]
    assert "email_address" in result[0]

def test_clean_csv_strips_whitespace():
    rows = [{"name": "  Carol  ", "email": " carol@example.com "}]
    result = clean_csv(rows)
    assert result[0]["name"] == "Carol"
    assert result[0]["email"] == "carol@example.com"

def test_clean_csv_empty_input_returns_empty():
    assert clean_csv([]) == []

def test_clean_csv_preserves_order():
    rows = [
        {"name": "Charlie", "email": "c@example.com"},
        {"name": "Alice",   "email": "a@example.com"},
        {"name": "Bob",     "email": "b@example.com"},
    ]
    result = clean_csv(rows)
    assert [r["name"] for r in result] == ["Charlie", "Alice", "Bob"]


# ── load_csv / save_csv (file I/O) ────────────────────────────────────────────

def test_load_csv_raises_on_missing_file():
    with pytest.raises(FileNotFoundError):
        load_csv(Path("nonexistent_file.csv"))

def test_save_csv_raises_on_empty_rows(tmp_path):
    with pytest.raises(ValueError):
        save_csv([], tmp_path / "output.csv")

def test_save_and_load_roundtrip(tmp_path):
    rows = [
        {"name": "Alice", "email": "alice@example.com"},
        {"name": "Bob",   "email": "bob@example.com"},
    ]
    output = tmp_path / "test_output.csv"
    save_csv(rows, output)
    loaded = load_csv(output)
    assert loaded == rows