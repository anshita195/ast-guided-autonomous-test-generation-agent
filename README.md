# AST guided autonomous test generation agent

An AI-powered test generation platform that automatically creates comprehensive unit test suites for Python and JavaScript code using Google's Gemini AI. The system analyzes source code, generates intelligent test cases, executes them, and provides detailed coverage reports.

## Features

- **Multi-language Support**: Generates tests for Python (pytest) and JavaScript (Jest)
- **AI-Powered Generation**: Uses Google Gemini 2.0 Flash for intelligent test case creation
- **AST-based Parsing**: Extracts function metadata using Python's AST module and Acorn for JavaScript
- **Automated Execution**: Runs generated tests and provides pass/fail results
- **Coverage Reporting**: Detailed coverage analysis with percentage metrics
- **RESTful API**: Clean FastAPI backend with comprehensive error handling
- **Schema Validation**: Robust LLM interaction with retry logic for reliable outputs

## Architecture

The system operates as a four-stage pipeline:

1. **Parse & Understand**: Extracts functions, arguments, and metadata from source code
2. **Plan & Reason**: AI analyzes code and generates structured test plans
3. **Generate**: Creates executable test files (pytest for Python, Jest for JavaScript)
4. **Execute & Report**: Runs tests and generates coverage reports

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AgentForce_TestGen
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install JavaScript dependencies**
   ```bash
   npm install
   cd js && npm install
   ```

5. **Start the server**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`

## Usage

### API Endpoints

#### Generate Tests
```http
POST /generate
Content-Type: multipart/form-data

Parameters:
- language: "python" or "javascript"
- file: Source code file (.py or .js)
```

#### Health Check
```http
GET /health
```

### Example Usage

#### Python Example

**Input file** (`examples/sample_input.py`):
```python
def calculate_discount(items: list) -> float:
    """Calculate total discount for a shopping cart"""
    if not items:
        return 0.0
        
    total = sum(price * qty for price, qty in items)
    
    if total > 100:
        return total * 0.1
    return 0.0
```

**API Call**:
```bash
curl -X POST "http://localhost:8000/generate" \
  -F "language=python" \
  -F "file=@examples/sample_input.py"
```

**Response**:
```json
{
  "language": "python",
  "message": "Python tests generated and executed successfully",
  "test_file_path": "tests/tmp_abc123.py",
  "functions_found": 1,
  "coverage_report": {
    "status": "Success",
    "summary": "13 tests passed.",
    "coverage_percentage": 5.11,
    "full_log": "..."
  }
}
```

#### JavaScript Example

**Input file** (`examples/sample_input.js`):
```javascript
function calculateFactorial(n) {
  if (n < 0) return -1;
  if (n === 0) return 1;
  return n * calculateFactorial(n - 1);
}
```

**API Call**:
```bash
curl -X POST "http://localhost:8000/generate" \
  -F "language=javascript" \
  -F "file=@examples/sample_input.js"
```

**Response**:
```json
{
  "language": "javascript",
  "message": "JavaScript tests generated and executed successfully",
  "test_file_path": "js_tests/tmp_def456.test.js",
  "functions_found": 1,
  "coverage_report": {
    "status": "Success",
    "summary": "8 tests passed out of 8.",
    "coverage_percentage": 100.0,
    "full_log": "..."
  }
}
```

## Project Structure

```
AgentForce_TestGen/
├── app/                    # Core application
│   ├── main.py            # FastAPI server and endpoints
│   ├── parser.py          # Python AST parser
│   ├── js_parser.py       # JavaScript parser wrapper
│   ├── test_generator.py  # Python test file generator
│   ├── js_test_generator.py # JavaScript test file generator
│   ├── llm.py             # Google Gemini AI integration
│   ├── runner.py          # Python test execution and coverage
│   └── js_runner.py       # JavaScript test execution and coverage
├── examples/              # Sample input files
│   ├── sample_input.py    # Python example
│   └── sample_input.js    # JavaScript example
├── js/                    # JavaScript dependencies and parser
│   ├── parser.js          # Node.js AST parser script
│   ├── package.json       # JS dependencies (acorn)
│   └── node_modules/      # Acorn installation
├── tests/                 # Generated Python tests (auto-created)
├── js_tests/              # Generated JavaScript tests (auto-created)
├── coverage/              # Coverage reports (auto-generated)
├── requirements.txt       # Python dependencies
├── package.json          # Root JS dependencies (jest)
├── .env.example          # Environment template
└── README.md             # This file
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |

### API Configuration

The API supports the following languages:
- `python`: Generates pytest-compatible tests
- `javascript`: Generates Jest-compatible tests

## Testing

Run the comprehensive test suite:

```bash
python examples/test_api.py
```

This will test:
- API health and connectivity
- Python test generation and execution
- JavaScript test generation and execution
- Error handling and validation

## Coverage Reports

The system provides detailed coverage analysis:

- **Python**: Uses `pytest-cov` for line coverage analysis
- **JavaScript**: Uses Jest's built-in coverage reporting
- **Output**: JSON summaries with percentage metrics
- **Format**: Industry-standard coverage.xml (Python) and coverage-summary.json (JavaScript)

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Troubleshooting

### Common Issues

1. **"GEMINI_API_KEY not found"**
   - Ensure you have a `.env` file with your API key
   - Verify the API key is valid and active

2. **"Jest not found"**
   - Run `npm install` to install JavaScript dependencies
   - Ensure Node.js 16+ is installed

3. **"Import errors"**
   - Install Python dependencies: `pip install -r requirements.txt`
   - Verify Python 3.8+ is installed

4. **"Tests failing"**
   - Check that source files are in the `examples/` directory
   - Verify function names match between source and generated tests

### Debug Mode

Run with verbose logging:
```bash
python -m uvicorn app.main:app --reload --log-level debug
```

## Technical Details

### AI Integration
- Uses Google Gemini 2.0 Flash for test generation
- Implements schema validation with retry logic
- Structured prompts for consistent JSON output

### Code Analysis
- **Python**: Built-in AST module for function extraction
- **JavaScript**: Acorn parser via Node.js subprocess
- Extracts function names, parameters, and metadata

### Test Execution
- **Python**: pytest with coverage.py integration
- **JavaScript**: Jest with built-in coverage reporting
- Automated cleanup of temporary test files

## License

This project is licensed under the MIT License.

## Acknowledgments

- Google Gemini AI for intelligent test generation
- FastAPI for the robust API framework
- pytest and Jest for test execution
- The open-source community for various dependencies
