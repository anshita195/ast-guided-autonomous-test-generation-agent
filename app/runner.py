import subprocess
import re
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

def get_coverage_from_xml(xml_path: str) -> float:
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        line_rate_str = root.get("line-rate")
        if line_rate_str:
            return round(float(line_rate_str) * 100, 2)
        return 0.0
    except (ET.ParseError, FileNotFoundError):
        return 0.0

def run_tests_and_get_coverage(test_file_path: str, module_name: str) -> dict:
    try:
        project_root = Path(__file__).parent.parent
        coverage_xml_path = project_root / "coverage.xml"

        command = [
            sys.executable,
            "-m", "pytest",
            test_file_path,
            f"--cov={project_root / 'examples'}",
            f"--cov-report=xml:{coverage_xml_path}",
            "-v"
        ]

        # --- FIX: Handle Windows-specific encoding ---
        # Run the process and attempt to decode output, with a fallback for Windows
        result = subprocess.run(
            command,
            capture_output=True,
            check=True,  # We'll handle the exception below
            cwd=project_root,
            timeout=30  # Add timeout to prevent hanging
        )
        try:
            output = result.stdout.decode('utf-8')
        except UnicodeDecodeError:
            output = result.stdout.decode('cp1252') # Fallback for Windows console

        passed_match = re.search(r"(\d+)\s+passed", output)
        summary = f"{passed_match.group(1) if passed_match else '0'} tests passed."
        coverage_pct = get_coverage_from_xml(str(coverage_xml_path))

        return {
            "status": "Success",
            "summary": summary,
            "coverage_percentage": coverage_pct,
            "full_log": output
        }

    except subprocess.CalledProcessError as e:
        stdout = (e.stdout or b"").decode('utf-8', errors='ignore')
        stderr = (e.stderr or b"").decode('utf-8', errors='ignore')
        
        # Try to get coverage even if tests failed
        coverage_pct = 0.0
        if coverage_xml_path.exists():
            coverage_pct = get_coverage_from_xml(str(coverage_xml_path))
        
        return {
            "status": "Tests Failed",
            "summary": "Pytest execution failed.",
            "coverage_percentage": coverage_pct,
            "error": "Pytest process returned a non-zero exit code.",
            "full_log": stdout + stderr
        }
    except Exception as e:
        return {
            "status": "Error",
            "summary": "An unexpected error occurred during test execution.",
            "coverage_percentage": 0.0,
            "error": str(e)
        }