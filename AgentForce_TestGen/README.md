# AgentForce TestGen

🤖 **AI-Powered Test Case Generator for Python and JavaScript**

AgentForce TestGen is a sophisticated tool that automatically generates comprehensive test cases for your Python and JavaScript functions using Google's Gemini AI. It analyzes your code, generates meaningful test cases, and provides detailed coverage reports.

## ✨ Features

- 🐍 **Python Support**: Generates pytest-compatible test cases
- 🟨 **JavaScript Support**: Generates Jest-compatible test cases
- 🧠 **AI-Powered**: Uses Google Gemini 2.0 Flash for intelligent test generation
- 📊 **Coverage Reports**: Detailed test coverage analysis
- 🚀 **FastAPI Backend**: RESTful API for easy integration
- 🎯 **Smart Parsing**: AST-based code analysis for accurate function extraction

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Google Gemini API Key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AgentForce_TestGen
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install JavaScript dependencies**
   ```bash
   npm install
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

5. **Start the server**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`

## 📖 Usage

### API Endpoints

#### Generate Tests
```http
POST /generate
Content-Type: multipart/form-data

Parameters:
- language: "python" or "javascript"
- file: Your source code file (.py or .js)
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

**Generated test**:
```python
import pytest
from examples import sample_input

def test_sample_input_1():
    # Test with input: []
    result = sample_input.calculate_discount([])
    assert result == pytest.approx(0.0)

def test_sample_input_2():
    # Test with input: [(50, 1), (60, 1)]
    result = sample_input.calculate_discount([(50, 1), (60, 1)])
    assert result == pytest.approx(11.0)
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

**Generated test**:
```javascript
const { calculateFactorial } = require('../examples/sample_input');

describe('calculateFactorial', () => {
  it('should return 1 for factorial of 0', () => {
    expect(calculateFactorial(0)).toBe(1);
  });
  it('should return 120 for factorial of 5', () => {
    expect(calculateFactorial(5)).toBe(120);
  });
});
```

### Using the API

#### cURL Example
```bash
curl -X POST "http://localhost:8000/generate" \
  -F "language=python" \
  -F "file=@examples/sample_input.py"
```

#### Python Example
```python
import requests

url = "http://localhost:8000/generate"
files = {"file": open("examples/sample_input.py", "rb")}
data = {"language": "python"}

response = requests.post(url, files=files, data=data)
result = response.json()
print(f"Coverage: {result['coverage_report']['coverage_percentage']}%")
```

## 🏗️ Architecture

```
AgentForce TestGen/
├── app/                    # FastAPI application
│   ├── main.py            # Main API endpoints
│   ├── parser.py          # Python AST parser
│   ├── js_parser.py       # JavaScript parser wrapper
│   ├── test_generator.py  # Python test generator
│   ├── js_test_generator.py # JavaScript test generator
│   ├── llm.py             # Google Gemini integration
│   ├── runner.py          # Python test runner
│   └── js_runner.py       # JavaScript test runner
├── examples/              # Sample input files
├── tests/                 # Generated Python tests
├── js_tests/              # Generated JavaScript tests
├── js/                    # Node.js parser script
└── coverage/              # Coverage reports
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes | - |
| `FASTAPI_HOST` | API host | No | `0.0.0.0` |
| `FASTAPI_PORT` | API port | No | `8000` |
| `FASTAPI_RELOAD` | Auto-reload | No | `true` |

### API Configuration

The API supports the following languages:
- `python`: Generates pytest-compatible tests
- `javascript`: Generates Jest-compatible tests

## 📊 Test Coverage

AgentForce TestGen provides comprehensive coverage reporting:

- **Python**: Uses `pytest-cov` for coverage analysis
- **JavaScript**: Uses Jest's built-in coverage reporting
- **Metrics**: Line coverage percentage and detailed reports
- **Output**: JSON summaries and HTML reports

## 🧪 Testing

Run the existing test suite:

```bash
# Python tests
python -m pytest tests/ -v

# JavaScript tests
npx jest js_tests/ --verbose
```

## 🛠️ Development

### Project Structure

- **Parsers**: Extract function information from source code
- **LLM Integration**: Generate test cases using Google Gemini
- **Test Generators**: Create executable test files
- **Runners**: Execute tests and collect coverage
- **API Layer**: RESTful interface for all functionality

### Adding New Languages

1. Create a parser for the new language
2. Implement a test generator
3. Add a test runner
4. Update the API endpoint

## 📝 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🐛 Troubleshooting

### Common Issues

1. **"GEMINI_API_KEY not found"**
   - Ensure you have a `.env` file with your API key
   - Verify the API key is valid

2. **"Jest not found"**
   - Run `npm install` to install JavaScript dependencies

3. **"Import errors"**
   - Ensure all Python dependencies are installed: `pip install -r requirements.txt`

4. **"Tests failing"**
   - Check that your source files are in the `examples/` directory
   - Verify the function names match between source and tests

### Debug Mode

Run with debug logging:
```bash
python -m uvicorn app.main:app --reload --log-level debug
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini AI for intelligent test generation
- FastAPI for the robust API framework
- Jest and pytest for test execution
- The open-source community for various dependencies

---

**Made with ❤️ by AgentForce Team**
