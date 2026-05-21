# CSV Cleaner

A lightweight Python utility that reads a CSV file, applies common data-cleaning steps, and writes a cleaned output file.

Built with clean code practices in mind: type hints throughout, structured logging, proper error handling, and a full pytest test suite. Dependencies are managed with [uv](https://docs.astral.sh/uv/) for fast, reproducible installs.

---

## What it does

| Step | Description |
|------|-------------|
| Normalize headers | Strips whitespace, lowercases, replaces spaces with underscores |
| Strip whitespace | Trims leading/trailing spaces from every cell value |
| Drop empty rows | Removes rows where all values are blank |
| Remove duplicates | Deduplicates rows while preserving original order |

---

## Project structure

```
csv_cleaner/
├── cleaner.py          # Main script — load, clean, save pipeline
├── test_cleaner.py     # 18 pytest unit tests
├── pyproject.toml      # Project metadata and dependencies
├── uv.lock             # Exact dependency versions (auto-generated)
├── Dockerfile          # Container definition (uses uv)
└── docker-compose.yml  # Shortcuts for running tests and the cleaner
```

---

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) — install with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Usage

### Run locally with uv

```bash
# Install dependencies (creates .venv automatically)
uv sync

# Clean a CSV file
uv run python cleaner.py input.csv output.csv

# Run tests
uv run pytest test_cleaner.py -v
```

### Run with Docker

**Build the image:**
```bash
docker build -t csv-cleaner .
```

**Run the test suite:**
```bash
docker run --rm csv-cleaner
```

**Clean a file (mount your local `data/` folder):**
```bash
# Place your input.csv inside data/, then:
docker run --rm -v $(pwd)/data:/app/data csv-cleaner \
  uv run python cleaner.py data/input.csv data/output.csv
```

### Run with Docker Compose

```bash
# Run tests
docker compose run test

# Clean a file (reads data/input.csv, writes data/output.csv)
docker compose run clean
```

---

## Example

**Input (`data/input.csv`):**
```
First Name, Email Address
Alice, alice@example.com
Bob , bob@example.com
Alice, alice@example.com
,
```

**Output (`data/output.csv`):**
```
first_name,email_address
Alice,alice@example.com
Bob,bob@example.com
```

---

## Logging

Logs to both the console and `cleaner.log` in the working directory.

```
2025-05-21 10:00:01 [INFO] Loaded 4 rows from 'input.csv'
2025-05-21 10:00:01 [INFO] Dropped 1 empty row(s).
2025-05-21 10:00:01 [INFO] Dropped 1 duplicate row(s).
2025-05-21 10:00:01 [INFO] Cleaning complete. 2 row(s) remaining.
2025-05-21 10:00:01 [INFO] Saved cleaned CSV to 'output.csv'
```

---

## License

MIT