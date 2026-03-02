import ast
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class FunctionInfo:
    name: str
    args: List[str]
    docstring: Optional[str]
    complexity: str
    imports: List[str]

class CodeParser:
    def parse_file(self, content: str) -> List[FunctionInfo]:
        tree = ast.parse(content)
        functions = []
        
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    imports.extend(n.name for n in node.names)
                else:
                    imports.extend(f"{node.module}.{n.name}" for n in node.names)

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                functions.append(FunctionInfo(
                    name=node.name,
                    args=[arg.arg for arg in node.args.args],
                    docstring=ast.get_docstring(node),
                    complexity=self._estimate_complexity(node),
                    imports=imports
                ))
        
        return functions

    def _estimate_complexity(self, node: ast.FunctionDef) -> str:
        loops = len([n for n in ast.walk(node) if isinstance(n, (ast.For, ast.While))])
        if loops > 1:
            return "O(n^2)" if any(
                isinstance(n, ast.For) for n in ast.walk(node)
            ) else "O(n)"
        return "O(1)"