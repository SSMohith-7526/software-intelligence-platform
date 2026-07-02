import ast
from typing import Dict, Any
from utils.logger import logger

class ASTBuilder:
    """Constructs the high-level semantic representation of the parsed code."""
    
    @staticmethod
    def build_summary(code_content: str, filename: str) -> Dict[str, Any]:
        """Extracts class and function definitions for the Context Bus."""
        summary = {
            "functions": [],
            "classes": [],
            "imports": [],
            "syntax_valid": True
        }
        
        try:
            parsed_tree = ast.parse(code_content, filename=filename)
            for node in ast.walk(parsed_tree):
                if isinstance(node, ast.FunctionDef):
                    args = [arg.arg for arg in node.args.args]
                    summary["functions"].append({"name": node.name, "args": args, "line": node.lineno})
                elif isinstance(node, ast.ClassDef):
                    summary["classes"].append({"name": node.name, "line": node.lineno})
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    summary["imports"].append(ast.unparse(node))
            return summary
        except SyntaxError:
            # Handled upstream by the Parser, but caught here for safety
            summary["syntax_valid"] = False
            return summary