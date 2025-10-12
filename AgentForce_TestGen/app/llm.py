import os
import google.generativeai as genai
from typing import Dict, List, Any
from dotenv import load_dotenv
from pathlib import Path
import json
import re
from jsonschema import validate, ValidationError
from .parser import FunctionInfo

# --- MODIFIED PYTHON SCHEMA ---
PY_TEST_SCHEMA = {
    "type": "object",
    "properties": {
        "test_groups": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    # --- ADDED: Explicitly require the function name ---
                    "function_name": {"type": "string"},
                    "cases": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "input": {"type": "string"},
                                "expected_output": {"type": ["string", "number", "boolean"]}
                            },
                            "required": ["input", "expected_output"]
                        }
                    }
                },
                # --- ADDED: Make function_name a required property ---
                "required": ["function_name", "cases"]
            }
        }
    },
    "required": ["test_groups"]
}

JS_TEST_SCHEMA = {
    "type": "object",
    "properties": {
        "imports": {"type": "string"},
        "tests": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "describe": {"type": "string"},
                    "cases": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "it": {"type": "string"},
                                "function_to_test": {"type": "string"},
                                "input": {"type": "string"},
                                "expected_output": {"type": ["string", "number", "boolean"]}
                            },
                            "required": ["it", "function_to_test", "input", "expected_output"]
                        }
                    }
                },
                "required": ["describe", "cases"]
            }
        }
    },
    "required": ["imports", "tests"]
}


class LLMWrapper:
    def __init__(self, max_retries=3):
        env_path = Path(__file__).parent.parent / '.env'
        load_dotenv(env_path)
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.max_retries = max_retries

    def _generate_and_validate(self, prompt: str, schema: Dict) -> str:
        """Main generation loop with validation and retries."""
        for attempt in range(self.max_retries):
            try:
                generation_config = {"temperature": 0.4, "top_k": 1, "max_output_tokens": 2048}
                response = self.model.generate_content(
                    contents=[{"parts": [{"text": prompt}]}],
                    generation_config=generation_config
                )
                raw_text = response.text.strip()
                json_match = re.search(r'```json\s*({[\s\S]*?})\s*```|({[\s\S]*})', raw_text)
                if not json_match:
                    raise ValueError("No JSON object found in the LLM response.")
                json_str = next(group for group in json_match.groups() if group is not None)
                parsed_json = json.loads(json_str)
                validate(instance=parsed_json, schema=schema)
                return json.dumps(parsed_json)
            except (ValueError, json.JSONDecodeError, ValidationError) as e:
                print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                prompt += f"\n\nYour previous response failed validation with the error: {e}. \nPlease correct your response and ensure it strictly adheres to this JSON schema:\n{json.dumps(schema)}"
        raise RuntimeError(f"Failed to generate valid JSON after {self.max_retries} attempts.")

    # --- PYTHON METHODS ---
    def generate_tests(self, code: str, functions: List[FunctionInfo]) -> str:
        prompt = self._build_py_prompt(code, functions)
        return self._generate_and_validate(prompt, PY_TEST_SCHEMA)

    def _build_py_prompt(self, code: str, functions: List[FunctionInfo]) -> str:
        function_info_str = "\n".join(
            f"- {f.name}({', '.join(f.args)}): {f.docstring or 'No docstring'}"
            for f in functions
        )
        # --- MODIFIED: Update prompt to ask for the function_name key ---
        return f"""You are an expert test engineer. Analyze the Python code and generate test cases.
Your response MUST be a single JSON object.

For each function, create a "test_group" that includes the "function_name" and a list of "cases".

**CRITICAL INSTRUCTIONS**: 
1. The `input` key must be a STRING representation of the input (e.g., "2", "hello", "[1,2,3]")
2. The `expected_output` key must contain ONLY the raw expected value (e.g., `4`, `"Hello"`, `true`)

Example format:
{{
  "test_groups": [
    {{
      "function_name": "add",
      "cases": [
        {{"input": "2", "expected_output": 4}},
        {{"input": "0", "expected_output": 0}}
      ]
    }}
  ]
}}

Code to analyze:
{code}

Function information:
{function_info_str}
"""

    # --- JAVASCRIPT METHODS ---
    def generate_js_tests(self, code: str, functions: List[Dict]) -> str:
        prompt = self._build_js_prompt(code, functions)
        return self._generate_and_validate(prompt, JS_TEST_SCHEMA)

    def _build_js_prompt(self, code: str, functions: List[Dict]) -> str:
        function_info_str = "\n".join(
            f"- {f['name']}({', '.join(f['args'])})"
            for f in functions
        )
        return f"""You are an expert test engineer. Analyze the JavaScript code and generate Jest test cases.
Your response MUST be a single JSON object.

**CRITICAL INSTRUCTION**: The `expected_output` key must contain ONLY the raw expected value (e.g., `1`, `-1`, or a string like `"Hello, World!"`). DO NOT include any code, functions, or expressions like `.toBe(1)`.

Code to analyze:
{code}
Function information:
{function_info_str}
"""