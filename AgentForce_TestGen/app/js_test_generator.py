from pathlib import Path
from typing import Dict, List, Any
import re
import tempfile

class JSTestGenerator:
    def __init__(self, output_dir: str = "js_tests"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def _format_js_value(self, value: Any) -> str:
        if isinstance(value, str):
            escaped_value = value.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
            return f"`{escaped_value}`"
        if isinstance(value, bool):
            return "true" if value else "false"
        if value is None:
            return "null"
        return str(value)

    def generate_test_file(self, module_name: str, test_data: Dict) -> str:
        # (The rest of the function remains the same...)
        test_content = []

        try:
            function_names_str = re.search(r'\{\s*(.*?)\s*\}', test_data["imports"]).group(1)
            imports_line = f"const {{ {function_names_str} }} = require('../examples/{module_name}');"
        except (AttributeError, IndexError):
            imports_line = f"// Failed to automatically generate imports. Please check manually."

        test_content.append(imports_line)
        test_content.append("")

        for test_suite in test_data.get("tests", []):
            describe_name = test_suite.get("describe", "Test Suite")
            test_content.append(f"describe('{describe_name}', () => {{")

            for case in test_suite.get("cases", []):
                if not all(k in case for k in ["it", "function_to_test", "input", "expected_output"]):
                    continue

                it_desc = case["it"]
                func_name = case["function_to_test"]
                input_val = case["input"]
                expected_out = case["expected_output"]

                formatted_expected = self._format_js_value(expected_out)

                if isinstance(expected_out, (dict, list)):
                    assertion = f"expect({func_name}({input_val})).toEqual({formatted_expected});"
                else:
                    assertion = f"expect({func_name}({input_val})).toBe({formatted_expected});"

                test_content.extend([
                    f"  it('{it_desc.replace("'", "\\'")}', () => {{",
                    f"    {assertion}",
                    "  });"
                ])

            test_content.append("});")
            test_content.append("")

        # --- FIX: Ensure the temporary file has the .test.js suffix ---
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.test.js', delete=False, dir=self.output_dir, encoding='utf-8') as temp_file:
            temp_file.write("\n".join(test_content))
            return temp_file.name