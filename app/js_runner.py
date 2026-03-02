import subprocess
import json
from pathlib import Path
from typing import Dict, Any

def run_js_tests_and_get_coverage(test_file_path: str, module_name: str) -> Dict[str, Any]:
    """
    Runs Jest with coverage and returns a parsed report.
    """
    try:
        project_root = Path(__file__).parent.parent
        jest_cli_path = project_root / "node_modules" / "jest" / "bin" / "jest.js"

        if not jest_cli_path.exists():
            raise FileNotFoundError("jest.js not found. Please run 'npm install jest'.")

        # --- FIX: Use a relative path for the coverage collection ---
        # This is more robust for Jest across different platforms.
        source_file_relative = f"examples/{module_name}.js"
        
        results_path = project_root / 'jest_results.json'
        coverage_summary_path = project_root / "coverage" / "coverage-summary.json"

        command = [
            "node",
            str(jest_cli_path),
            test_file_path,
            "--coverage",
            # Use the relative path here
            f"--collectCoverageFrom={source_file_relative}",
            "--coverageReporters=json-summary",
            "--json",
            f"--outputFile={results_path}"
        ]

        subprocess.run(
            command,
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )

        with open(results_path, 'r', encoding='utf-8') as f:
            results = json.load(f)

        coverage_pct = 0.0
        if coverage_summary_path.exists():
            with open(coverage_summary_path, 'r', encoding='utf-8') as f:
                coverage_data = json.load(f)
                coverage_pct = coverage_data.get("total", {}).get("lines", {}).get("pct", 0.0)

        if results_path.exists():
            results_path.unlink()

        summary = f"{results.get('numPassedTests', 0)} tests passed out of {results.get('numTotalTests', 0)}."

        return {
            "status": "Success" if results.get('numFailedTests', 0) == 0 else "Tests Failed",
            "summary": summary,
            "coverage_percentage": coverage_pct,
            "full_log": results
        }

    except subprocess.CalledProcessError as e:
        stdout = (e.stdout or b"").decode('utf-8', errors='ignore')
        stderr = (e.stderr or b"").decode('utf-8', errors='ignore')
        return {
            "status": "Error",
            "summary": "Jest execution failed.",
            "error": "Jest process returned a non-zero exit code.",
            "full_log": stdout + stderr
        }
    except Exception as e:
        return {
            "status": "Error",
            "summary": "An unexpected error occurred during test execution.",
            "error": str(e)
        }