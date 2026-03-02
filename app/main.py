from fastapi import FastAPI, File, UploadFile, Form, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import os
import logging
from pathlib import Path
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Python Tools ---
from .parser import CodeParser  # <-- THIS LINE WAS MISSING
from .llm import LLMWrapper
from .test_generator import TestGenerator
from .runner import run_tests_and_get_coverage

# --- JavaScript Tools ---
from .js_parser import parse_js_file
from .js_test_generator import JSTestGenerator
from .js_runner import run_js_tests_and_get_coverage

# --- Compatibility Function ---
def map_test_cases_to_new_schema(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    If the old 'test_cases' format is detected, map it to the new schema.
    """
    if "test_cases" in data and "tests" not in data:
        describes = {}
        for case in data["test_cases"]:
            func_name = case["function"]
            if func_name not in describes:
                describes[func_name] = {
                    "describe": func_name,
                    "cases": []
                }
            describes[func_name]["cases"].append({
                "it": f"should handle input {case['input']}",
                "function_to_test": func_name,
                "input": str(case['input']),
                "expected_output": case['expected_output']
            })
        
        func_names = ", ".join(describes.keys())

        return {
            "imports": f"const {{ {func_names} }} = require('../examples/sample_input');",
            "tests": list(describes.values())
        }
    return data

app = FastAPI(
    title="AgentForce TestGen",
    description="AI-powered test case generator for Python and JavaScript",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Tool Instances ---
py_parser = CodeParser()
py_test_gen = TestGenerator()
js_test_gen = JSTestGenerator()

# Initialize LLM wrapper with error handling
try:
    llm = LLMWrapper()
    logger.info("LLM wrapper initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize LLM wrapper: {e}")
    llm = None

@app.get("/")
async def root():
    """Root endpoint with basic information"""
    return {
        "message": "AgentForce TestGen API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "generate": "/generate",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    llm_status = "available" if llm is not None else "unavailable"
    return {
        "status": "healthy",
        "llm": llm_status,
        "timestamp": "2025-01-10T00:00:00Z"
    }

@app.post("/generate")
async def generate_tests(
    language: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Generate test cases for an uploaded file in the specified language.
    
    - **language**: Either "python" or "javascript"
    - **file**: Source code file (.py or .js)
    
    Returns:
    - Generated test file path
    - Coverage report
    - Test execution results
    """
    # Input validation
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
        )
    
    if not language:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Language parameter is required"
        )
    
    # Check LLM availability
    if llm is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM service is not available. Please check your GEMINI_API_KEY configuration."
        )
    
    # Validate language
    if language not in ["python", "javascript"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported language. Please choose 'python' or 'javascript'."
        )
    
    # Validate file type
    if language == "python" and not file.filename.endswith('.py'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="For Python, only .py files are supported"
        )
    
    if language == "javascript" and not file.filename.endswith('.js'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="For JavaScript, only .js files are supported"
        )
    
    try:
        # Read file content
        content_bytes = await file.read()
        if len(content_bytes) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty"
            )
        
        try:
            content_str = content_bytes.decode('utf-8')
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be encoded in UTF-8"
            )
        
        # Validate content length
        if len(content_str.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File contains no code"
            )
        
        module_name = Path(file.filename).stem
        
        if language == "python":
            return await process_python_file(content_str, module_name)
        else:  # javascript
            return await process_javascript_file(content_str, module_name)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing {language} file: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

async def process_python_file(content_str: str, module_name: str) -> Dict[str, Any]:
    """Process Python file and generate tests"""
    try:
        # Parse Python file
        functions = py_parser.parse_file(content_str)
        
        if not functions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No functions found in the Python file"
            )
        
        # Generate tests using LLM
        test_data_str = llm.generate_tests(content_str, functions)
        test_json = json.loads(test_data_str)
        
        # Generate test file
        test_file_path = py_test_gen.generate_test_file(module_name, test_json)
        
        # Run tests and get coverage
        coverage_results = run_tests_and_get_coverage(test_file_path, module_name)
        
        return {
            "language": "python",
            "message": "Python tests generated and executed successfully",
            "test_file_path": test_file_path,
            "functions_found": len(functions),
            "coverage_report": coverage_results
        }
        
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse LLM response as JSON: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing Python file: {str(e)}"
        )

async def process_javascript_file(content_str: str, module_name: str) -> Dict[str, Any]:
    """Process JavaScript file and generate tests"""
    try:
        # Parse JavaScript file
        js_functions = parse_js_file(content_str)
        
        if not js_functions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No functions found in the JavaScript file"
            )
        
        # Generate tests using LLM
        test_data_str = llm.generate_js_tests(content_str, js_functions)
        raw_json = json.loads(test_data_str)
        test_json = map_test_cases_to_new_schema(raw_json)
        
        # Generate test file
        test_file_path = js_test_gen.generate_test_file(module_name, test_json)
        
        # Run tests and get coverage
        coverage_results = run_js_tests_and_get_coverage(test_file_path, module_name)
        
        return {
            "language": "javascript",
            "message": "JavaScript tests generated and executed successfully",
            "test_file_path": test_file_path,
            "functions_found": len(js_functions),
            "coverage_report": coverage_results
        }
        
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse LLM response as JSON: {str(e)}"
        )
    except (RuntimeError, ValueError, FileNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing JavaScript file: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error processing JavaScript file: {str(e)}"
        )