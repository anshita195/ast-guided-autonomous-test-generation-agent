# TestGen AI Agent

**TestGen** is an intelligent developer agent that automates unit-test creation. It analyzes **Python** and **JavaScript** code, reasons about logic and edge cases, generates tests, executes them, and returns execution results plus code-coverage reports.

> Built for **Track 2: Developer Agents — Problem 1: Test Case Generator Bot**.

---

## Table of Contents

* [Features](#features)
* [Architecture](#architecture)
* [Quick Start](#quick-start)
* [Usage](#usage)
* [CLI flags used by runners (recommended)](#cli-flags-used-by-runners-recommended)
* [Project structure](#project-structure)
* [`.gitignore` suggestions](#gitignore-suggestions)
* [Limitations & Security (Important)](#limitations--security-important)
* [Troubleshooting & Tips](#troubleshooting--tips)
* [Contributing](#contributing)
* [License](#license)

---

## Features

* **Multi-language** support: Generates tests for **Python** (pytest) and **JavaScript** (Jest).
* **Intelligent test generation**: Produces tests covering logic paths and edge cases (empty inputs, zero, negative numbers, etc.).
* **Automated execution**: Runs generated tests and returns pass/fail results.
* **Machine-readable coverage**: Returns accurate coverage percentage (`coverage.xml` / `coverage.json` for Python, `coverage/coverage-summary.json` for JS).
* **FastAPI API**: Clean `/generate` endpoint for submitting files.
* **Resilient LLM interaction**: Schema validation + retry logic to keep AI outputs structured and reliable.

---

## Architecture (high-level)

TestGen operates as a four-step pipeline:

1. **Parse & Understand**

   * Python: uses the built-in `ast` module to extract functions, arguments, and docstrings.
   * JavaScript: uses `acorn` via a Node.js helper script to extract function metadata.

2. **Plan & Reason**

   * Structured metadata is sent to the generative AI (Google Gemini). A prompt instructs the model to return a JSON test plan conforming to a schema.

3. **Generate**

   * The validated JSON plan is transformed into a concrete test file (pytest for Python, Jest for JavaScript).

4. **Execute & Report**

   * The test runner executes the test file in a subprocess and writes machine-readable coverage outputs. The API responds with pass/fail summary and coverage percentage.

---

## Quick Start

### Prerequisites

* Python **3.10+**
* Node.js **14+** and `npm`
* A Google Gemini API key

### 1. Clone the repo

```bash
git clone <your-repository-url>
cd AgentForce_TestGen
```

### 2. Environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

### 3. Install dependencies

**Python dependencies**

```bash
pip install -r requirements.txt
```

**Node.js dependencies**

```bash
npm install
```

### 4. Run the server

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The API will be available at `http://127.0.0.1:8000`.

---

## Usage

Send a `POST` request to `/generate` with `language` and the `file` to analyze.

### Generate Python tests

```bash
curl -X POST \
  -F "language=python" \
  -F "file=@examples/sample_input.py" \
  http://127.0.0.1:8000/generate
```

**Example response (Python)**

```json
{
  "language": "python",
  "message": "Python tests generated and executed successfully",
  "test_file_path": "tests\\tmp_somefile.py",
  "coverage_report": {
    "status": "Success",
    "summary": "10 tests passed.",
    "coverage_percentage": 100.0,
    "full_log": "..."
  }
}
```

### Generate JavaScript tests

```bash
curl -X POST \
  -F "language=javascript" \
  -F "file=@examples/sample_input.js" \
  http://127.0.0.1:8000/generate
```

**Example response (JavaScript)**

```json
{
  "language": "javascript",
  "message": "JavaScript tests generated and executed successfully",
  "test_file_path": "js_tests\\tmp_somefile.test.js",
  "coverage_report": {
    "status": "Success",
    "summary": "8 tests passed out of 8.",
    "coverage_percentage": 100,
    "full_log": { ... }
  }
}
```

---

## CLI flags used by runners (recommended)

**Python (pytest + coverage)** — produce XML and JSON coverage:

```bash
# run tests and collect coverage (single command)
python -m coverage run -m pytest -q --maxfail=1 --disable-warnings --cov=examples --cov-report=xml:coverage.xml
# then export json coverage
python -m coverage json -o coverage.json
```

* `coverage.xml` contains `line-rate` (multiply by 100 → percent).
* `coverage.json` contains JSON-format coverage data if you prefer JSON.

**JavaScript (Jest)** — run tests + JSON test results + JSON coverage summary:

```bash
# run from project root (requires local jest installation)
node ./node_modules/jest/bin/jest.js --json --outputFile=jest_results.json --coverage --coverageReporters=json-summary --runInBand
```

* Read `coverage/coverage-summary.json` → `total.lines.pct` (or `statements.pct`) for coverage percent.
* `jest_results.json` contains structured test results and per-test details.
* `--runInBand` is recommended in ephemeral or resource-constrained sandboxes for predictability.

---

## Project structure

```
AgentForce_TestGen/
├── app/                  # Core application logic
│   ├── llm.py            # AI interaction, prompts, schema validation
│   ├── parser.py         # Python AST parser
│   ├── js_parser.py      # JS parser (Node.js wrapper)
│   ├── test_generator.py # Generates pytest files
│   ├── js_test_generator.py # Generates Jest files
│   ├── runner.py         # Executes pytest + generates coverage.xml/json
│   ├── js_runner.py      # Executes jest + reads coverage-summary.json
│   └── main.py           # FastAPI server and endpoints
├── examples/             # Sample input files (Python/JS)
├── js/                   # Node.js helper scripts (parser.js)
├── tests/                # Generated Python tests (ephemeral)
├── js_tests/             # Generated JS tests (ephemeral)
├── job_artifacts/        # Suggested output artifacts dir (not tracked)
├── .gitignore
├── requirements.txt
└── package.json
```

---

## Contributing

Contributions are welcome. Suggested priorities:

1. Add sandboxed execution (Docker / microVM) with resource limits.
2. Add a job queue (Redis + RQ/Celery) for asynchronous execution.
3. Add end-to-end CI tests and golden prompt tests to prevent prompt drift.
4. Improve observability (structured logs, job IDs, tracing, and metrics).

---

## Acknowledgements

* Uses Google Gemini (via `google-generativeai`) — ensure you comply with the model provider’s terms.
* Uses `pytest`, `pytest-cov`, and `coverage` for Python testing and coverage.
* Uses `jest` and its coverage reporters for JavaScript.

