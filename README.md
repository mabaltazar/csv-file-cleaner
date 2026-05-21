# CSV Cleaner

A Python script that takes a messy CSV file and cleans it up automatically — removing blank rows, fixing inconsistent headers, stripping extra spaces, and dropping duplicate entries.

---

## What it does

When you run this script on a CSV file, it applies four cleaning steps in order:

| Step | What it fixes |
|------|---------------|
| Normalize headers | Column names like `"  First Name  "` become `"first_name"` — no spaces, all lowercase |
| Strip whitespace | Cell values like `"  Alice  "` become `"Alice"` |
| Drop empty rows | Rows where every cell is blank are removed |
| Remove duplicates | If the same row appears more than once, only the first is kept |

---

## Project structure

Here's what each file in this project does:

```
csv-cleaner/
├── cleaner.py          # The main script that does the cleaning
├── test_cleaner.py     # Automated tests to verify the script works correctly
├── pyproject.toml      # Tells uv what dependencies to install
├── uv.lock             # Locks exact dependency versions for reproducible installs
├── Dockerfile          # Instructions for building a Docker container
├── docker-compose.yml  # Shortcuts for running the container
└── data/               # Put your CSV files here before running
```

---

## Requirements

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) — a fast Python package manager

### Installing uv

**Linux / macOS** — run this in your terminal:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows** — run these in PowerShell (the first line is a one-time permission fix):
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm https://astral.sh/uv/install.ps1 | iex
```

After installing, close and reopen your terminal, then verify it worked:
```bash
uv --version
```

---

## Usage

There are three ways to run this project: locally with uv, with Docker directly, or with Docker Compose.

---

### Option 1 — Run locally with uv

This is the simplest option if you just want to clean a file on your own machine.

```bash
# Step 1: Install dependencies (only needed once)
uv sync

# Step 2: Clean a CSV file
# Replace "your-file.csv" with your actual filename
uv run python cleaner.py your-file.csv output.csv

# The cleaned file will be saved as output.csv in the same folder
```

To run the tests and verify everything is working:
```bash
uv run pytest test_cleaner.py -v
```

---

### Option 2 — Run with Docker

Docker lets you run the script in an isolated container without worrying about Python versions or dependencies on your machine.

**Step 1 — Build the image** (only needed once, or after code changes):
```bash
docker build -t csv-cleaner .
```

**Step 2 — Run the test suite** to confirm the container works:
```bash
docker run --rm csv-cleaner
# You should see: 18 passed
```

**Step 3 — Clean a file**

Place your CSV file inside the `data/` folder first, then run:

**Linux / macOS:**
```bash
docker run --rm -v "$(pwd)/data:/app/data" csv-cleaner \
  uv run python cleaner.py data/your-file.csv data/output.csv
```

**Windows (Git Bash):**
```bash
MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd)/data:/app/data" csv-cleaner \
  uv run python cleaner.py data/your-file.csv data/output.csv
```

> **Why `MSYS_NO_PATHCONV=1` on Windows?**
> Git Bash on Windows automatically rewrites paths in commands, which breaks the Docker volume mount and creates a junk folder called `data;C` in your project. This prefix tells Git Bash to leave the paths alone.
>
> To avoid typing it every time, add it permanently to your shell:
> ```bash
> echo 'export MSYS_NO_PATHCONV=1' >> ~/.bashrc
> source ~/.bashrc
> ```
> After that, the regular command works with no prefix.

After the command runs, your cleaned file will appear as `data/output.csv` on your local machine.

---

### Option 3 — Run with Docker Compose

Docker Compose wraps the Docker commands into simple shortcuts.

**Before running the clean service**, open `docker-compose.yml` and update the filename to match your actual CSV:
```yaml
command: uv run python cleaner.py data/your-file.csv data/output.csv
```

Then:

```bash
# Run the test suite
docker compose run test

# Clean a file (reads from data/, writes output to data/)
docker compose run clean
```

If you see a warning about orphan containers, clean them up with:
```bash
docker compose down --remove-orphans
```
This happens when old containers from previous runs are still lingering — it's harmless but the cleanup keeps things tidy.

---

## Example

**Input (`data/sample-file.csv`):**
```
First Name, Email Address
Alice, alice@example.com
Bob , bob@example.com
Alice, alice@example.com
,
```

**Run:**
```bash
uv run python cleaner.py data/sample-file.csv data/output.csv
```

**Output (`data/output.csv`):**
```
first_name,email_address
Alice,alice@example.com
Bob,bob@example.com
```

What happened:
- `"First Name"` → `"first_name"` (header normalized)
- `"Bob "` → `"Bob"` (whitespace stripped)
- The duplicate Alice row was removed
- The empty row was removed

---

## Logging

Every run logs to both the terminal and a file called `cleaner.log` in your project folder. This means you always have a record of what was cleaned even after the terminal closes.

```
2026-05-21 10:00:01 [INFO] Loaded 4 rows from 'sample-file.csv'
2026-05-21 10:00:01 [INFO] Dropped 1 empty row(s).
2026-05-21 10:00:01 [INFO] Dropped 1 duplicate row(s).
2026-05-21 10:00:01 [INFO] Cleaning complete. 2 row(s) remaining.
2026-05-21 10:00:01 [INFO] Saved cleaned CSV to 'output.csv'
```

---

## Windows / Git Bash Troubleshooting

If you're on Windows using Git Bash, you may run into a few common issues:

| Symptom | Cause | Fix |
|---------|-------|-----|
| A folder called `data;C` appears in your project | Git Bash is mangling the Docker volume path | Add `export MSYS_NO_PATHCONV=1` to `~/.bashrc` |
| `uv: command not found` after installing | uv was installed but isn't on PATH yet | Close and reopen Git Bash, or reinstall uv via PowerShell |
| Warning about `VIRTUAL_ENV` path being wrong | A stale environment variable from a previous session | Run `unset VIRTUAL_ENV`, or remove it from `~/.bashrc` |
| `\\ uv: executable not found` error | Line continuation `\` has a trailing space after it | Run the docker command on a single line with no `\` |

---

## License

MIT