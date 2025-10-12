import json
from typing import Dict, Any
from pathlib import Path
import tempfile
import ast

class TestGenerator:
    def __init__(self, output_dir: str = "tests"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def _format_py_value(self, value: Any) -> str:
        if isinstance(value, str):
            return f"'{value.replace("'", "\\'")}'"
        return str(value)

    def generate_test_file(self, module_name: str, test_data: Dict) -> str:
        test_content = [
            "import pytest",
            "import sys",
            "import os",
            "sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'examples'))",
            f"import {module_name}",
            ""
        ]

        test_counter = 1
        # --- FINAL FIX: Use the function_name from the test group ---
        for group in test_data.get("test_groups", []):
            func_name = group.get("function_name")
            if not func_name:
                continue # Skip groups without a function name

            for case in group.get("cases", []):
                if "input" not in case or "expected_output" not in case:
                    continue

                try:
                    input_val = ast.literal_eval(case["input"])
                except (ValueError, SyntaxError):
                    continue
                
                expected_out = case["expected_output"]
                
                test_name = f"test_{module_name}_{test_counter}"
                test_counter += 1

                # Use the dynamic function name here
                test_content.extend([
                    f"def {test_name}():",
                    f"    # Test for {func_name} with input: {input_val}",
                    f"    result = {module_name}.{func_name}({input_val})",
                ])

                if isinstance(expected_out, float):
                    test_content.append(f"    assert result == pytest.approx({expected_out})")
                else:
                    formatted_expected = self._format_py_value(expected_out)
                    test_content.append(f"    assert result == {formatted_expected}")

                test_content.append("")

        temp_file = tempfile.NamedTemporaryFile(
            mode='w+',
            suffix='.py',
            delete=False,
            dir=self.output_dir,
            encoding='utf-8'
        )
        temp_file.write("\n".join(test_content))
        temp_file.close()
        return temp_file.name