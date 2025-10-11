# AgentForce TestGen API Documentation

## Overview

The AgentForce TestGen API provides endpoints for automatically generating test cases for Python and JavaScript code using AI-powered analysis.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. However, you need a valid `GEMINI_API_KEY` configured in your environment.

## Endpoints

### 1. Root Endpoint

**GET** `/`

Returns basic information about the API.

**Response:**
```json
{
  "message": "AgentForce TestGen API",
  "version": "1.0.0",
  "status": "running",
  "endpoints": {
    "generate": "/generate",
    "docs": "/docs",
    "health": "/health"
  }
}
```

### 2. Health Check

**GET** `/health`

Check the health status of the API and its dependencies.

**Response:**
```json
{
  "status": "healthy",
  "llm": "available",
  "timestamp": "2025-01-10T00:00:00Z"
}
```

**Possible LLM Status Values:**
- `"available"`: LLM service is properly configured
- `"unavailable"`: LLM service is not available (check GEMINI_API_KEY)

### 3. Generate Tests

**POST** `/generate`

Generate test cases for uploaded source code files.

**Content-Type:** `multipart/form-data`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `language` | string | Yes | Either "python" or "javascript" |
| `file` | file | Yes | Source code file (.py or .js) |

**Example Request (cURL):**
```bash
curl -X POST "http://localhost:8000/generate" \
  -F "language=python" \
  -F "file=@examples/sample_input.py"
```

**Example Request (Python):**
```python
import requests

url = "http://localhost:8000/generate"
files = {"file": open("examples/sample_input.py", "rb")}
data = {"language": "python"}

response = requests.post(url, files=files, data=data)
result = response.json()
```

**Success Response (Python):**
```json
{
  "language": "python",
  "message": "Python tests generated and executed successfully",
  "test_file_path": "tests/tmp_abc123.py",
  "functions_found": 1,
  "coverage_report": {
    "status": "Success",
    "summary": "11 tests passed.",
    "coverage_percentage": 100.0,
    "full_log": "..."
  }
}
```

**Success Response (JavaScript):**
```json
{
  "language": "javascript",
  "message": "JavaScript tests generated and executed successfully",
  "test_file_path": "js_tests/tmp_def456.test.js",
  "functions_found": 2,
  "coverage_report": {
    "status": "Success",
    "summary": "8 tests passed out of 8.",
    "coverage_percentage": 100.0,
    "full_log": "..."
  }
}
```

## Error Responses

### 400 Bad Request

**Invalid Language:**
```json
{
  "detail": "Unsupported language. Please choose 'python' or 'javascript'."
}
```

**Invalid File Type:**
```json
{
  "detail": "For Python, only .py files are supported"
}
```

**Empty File:**
```json
{
  "detail": "Uploaded file is empty"
}
```

**No Functions Found:**
```json
{
  "detail": "No functions found in the Python file"
}
```

### 503 Service Unavailable

**LLM Not Available:**
```json
{
  "detail": "LLM service is not available. Please check your GEMINI_API_KEY configuration."
}
```

### 500 Internal Server Error

**LLM Generation Failed:**
```json
{
  "detail": "Failed to parse LLM response as JSON: ..."
}
```

**Test Execution Failed:**
```json
{
  "detail": "Error processing Python file: ..."
}
```

## Rate Limits

Currently, no rate limits are implemented. However, be mindful of your Gemini API usage limits.

## File Size Limits

- Maximum file size: Not explicitly limited (depends on server configuration)
- Recommended maximum: 1MB for optimal performance
- Minimum content: File must contain at least one function

## Supported File Formats

### Python
- **Extension:** `.py`
- **Requirements:** Must contain at least one function definition
- **Output:** Pytest-compatible test files

### JavaScript
- **Extension:** `.js`
- **Requirements:** Must contain at least one function declaration
- **Output:** Jest-compatible test files

## Coverage Reports

The API provides detailed coverage reports for generated tests:

### Python Coverage
- Uses `pytest-cov` for coverage analysis
- Reports line coverage percentage
- Includes detailed test execution logs

### JavaScript Coverage
- Uses Jest's built-in coverage reporting
- Reports line coverage percentage
- Includes test suite execution details

## Interactive Documentation

When the server is running, you can access:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

These provide interactive documentation where you can test the API endpoints directly.

## Examples

### Complete Python Example

**Input File** (`math_utils.py`):
```python
def add_numbers(a, b):
    """Add two numbers and return the result."""
    return a + b

def multiply_numbers(a, b):
    """Multiply two numbers and return the result."""
    return a * b
```

**API Call:**
```bash
curl -X POST "http://localhost:8000/generate" \
  -F "language=python" \
  -F "file=@math_utils.py"
```

**Generated Test File:**
```python
import pytest
from examples import math_utils

def test_math_utils_1():
    result = math_utils.add_numbers(2, 3)
    assert result == 5

def test_math_utils_2():
    result = math_utils.multiply_numbers(4, 5)
    assert result == 20
```

### Complete JavaScript Example

**Input File** (`string_utils.js`):
```javascript
function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function reverse(str) {
    return str.split('').reverse().join('');
}

module.exports = { capitalize, reverse };
```

**API Call:**
```bash
curl -X POST "http://localhost:8000/generate" \
  -F "language=javascript" \
  -F "file=@string_utils.js"
```

**Generated Test File:**
```javascript
const { capitalize, reverse } = require('../examples/string_utils');

describe('capitalize', () => {
  it('should capitalize first letter', () => {
    expect(capitalize('hello')).toBe('Hello');
  });
});

describe('reverse', () => {
  it('should reverse string', () => {
    expect(reverse('hello')).toBe('olleh');
  });
});
```

## Troubleshooting

### Common Issues

1. **503 Service Unavailable**
   - Check if `GEMINI_API_KEY` is set in `.env`
   - Verify the API key is valid

2. **No functions found**
   - Ensure your file contains function definitions
   - Check file encoding (must be UTF-8)

3. **Test execution failed**
   - Verify your source file is in the `examples/` directory
   - Check for syntax errors in your source code

4. **Coverage issues**
   - Ensure all dependencies are installed
   - Check file paths and module imports

### Debug Mode

Enable debug logging by setting the log level:
```bash
python -m uvicorn app.main:app --reload --log-level debug
```
