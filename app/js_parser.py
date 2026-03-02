import subprocess
import json
from pathlib import Path
import tempfile
from typing import List, Dict, Any


def parse_js_file(file_content: str) -> List[Dict[str, Any]]:
    """
    Parses a JavaScript file using the external Node.js parser script.

    Args:
        file_content: The string content of the uploaded JS file.

    Returns:
        A list of dictionaries, where each dictionary contains info about a function.
    """
    # Create a temporary file to hold the JavaScript content
    # This is safer than relying on the original file path
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.js', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(file_content)
        temp_file_path = temp_file.name

    try:
        # Define the path to the Node.js parser script
        parser_script_path = Path(__file__).parent.parent / "js" / "parser.js"

        # Construct the command to run the Node.js script
        command = ["node", str(parser_script_path), temp_file_path]

        # Execute the command
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True # Raise an exception if the script fails
        )

        # Parse the JSON output from the script
        parsed_data = json.loads(result.stdout)
        return parsed_data.get("functions", [])

    except subprocess.CalledProcessError as e:
        # Handle cases where the Node.js script returns an error
        raise RuntimeError(f"JavaScript parser failed: {e.stderr}")
    except json.JSONDecodeError:
        # Handle cases where the output is not valid JSON
        raise ValueError("Could not decode JSON from JavaScript parser.")
    finally:
        # Clean up the temporary file
        if 'temp_file_path' in locals() and Path(temp_file_path).exists():
            Path(temp_file_path).unlink()