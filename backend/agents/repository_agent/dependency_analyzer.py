import ast
from typing import Dict, List
from utils.logger import logger

class DependencyAnalyzer:
    """Extracts internal and external module dependencies from source code."""
    
    @staticmethod
    def extract_imports(file_content: str, filepath: str) -> Dict[str, List[str]]:
        deps = {"standard": [], "internal": [], "third_party": []}
        
        if not filepath.endswith('.py'):
            return deps

        try:
            tree = ast.parse(file_content, filename=filepath)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        deps["standard"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module if node.module else "relative_import"
                    deps["standard"].append(module)
        except SyntaxError:
            logger.debug(f"Syntax error during dependency extraction in {filepath}.")
            
        return deps