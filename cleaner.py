"""
csv_cleaner/cleaner.py

Reads a CSV file, cleans common data issues, and writes a cleaned output file.

Cleaning steps:
  - Strip leading/trailing whitespace from all fields
  - Drop completely empty rows
  - Remove duplicate rows
  - Normalize column headers to lowercase with underscores
"""

import csv
import logging
from pathlib import Path

# Configure logging — writes to console AND a file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("cleaner.log"),
    ],
)
logger = logging.getLogger(__name__)


def normalize_header(header: str) -> str:
    """Normalize a column header to lowercase with underscores."""
    return header.strip().lower().replace(" ", "_")


def is_empty_row(row: dict[str, str]) -> bool:
    """Return True if all values in a row are empty strings."""
    return all(v.strip() == "" for v in row.values())


def clean_row(row: dict[str, str]) -> dict[str, str]:
    """Strip whitespace from every value in a row."""
    return {k: v.strip() for k, v in row.items()}


def load_csv(filepath: Path) -> list[dict[str, str]]:
    """
    Load a CSV file and return a list of row dicts.

    Raises:
        FileNotFoundError: if the file doesn't exist.
        ValueError: if the file is empty or has no headers.
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")

    with filepath.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            raise ValueError(f"CSV file has no headers: {filepath}")

        rows = list(reader)

    logger.info(f"Loaded {len(rows)} rows from '{filepath}'")
    return rows


def clean_csv(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """
    Apply all cleaning steps to a list of row dicts.

    Steps:
      1. Normalize headers
      2. Strip whitespace from values
      3. Drop empty rows
      4. Drop duplicate rows

    Returns the cleaned list of rows.
    """
    if not rows:
        logger.warning("No rows to clean.")
        return []

    # Step 1: Normalize headers
    normalized_rows = [
        {normalize_header(k): v for k, v in row.items()} for row in rows
    ]

    # Step 2: Strip whitespace
    cleaned = [clean_row(row) for row in normalized_rows]

    # Step 3: Drop empty rows
    before_empty = len(cleaned)
    cleaned = [row for row in cleaned if not is_empty_row(row)]
    dropped_empty = before_empty - len(cleaned)
    if dropped_empty:
        logger.info(f"Dropped {dropped_empty} empty row(s).")

    # Step 4: Drop duplicates (preserve order)
    seen: set[tuple] = set()
    deduped: list[dict[str, str]] = []
    for row in cleaned:
        key = tuple(row.items())
        if key not in seen:
            seen.add(key)
            deduped.append(row)

    dropped_dupes = len(cleaned) - len(deduped)
    if dropped_dupes:
        logger.info(f"Dropped {dropped_dupes} duplicate row(s).")

    logger.info(f"Cleaning complete. {len(deduped)} row(s) remaining.")
    return deduped


def save_csv(rows: list[dict[str, str]], filepath: Path) -> None:
    """
    Write a list of row dicts to a CSV file.

    Raises:
        ValueError: if rows is empty.
    """
    if not rows:
        raise ValueError("No rows to write — output file not created.")

    filepath.parent.mkdir(parents=True, exist_ok=True)

    with filepath.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    logger.info(f"Saved cleaned CSV to '{filepath}'")


def process(input_path: str, output_path: str) -> int:
    """
    Full pipeline: load → clean → save.

    Returns the number of rows written.
    Raises exceptions on file or data errors.
    """
    try:
        rows = load_csv(Path(input_path))
        cleaned = clean_csv(rows)
        save_csv(cleaned, Path(output_path))
        return len(cleaned)
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        raise
    except ValueError as e:
        logger.error(f"Data error: {e}")
        raise


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python cleaner.py <input.csv> <output.csv>")
        sys.exit(1)

    count = process(sys.argv[1], sys.argv[2])
    print(f"\nDone! {count} clean row(s) written to '{sys.argv[2]}'")