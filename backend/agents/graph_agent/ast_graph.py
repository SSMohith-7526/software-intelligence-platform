from typing import Dict, Any, List
from utils.logger import logger

class ASTGraphBuilder:
    """Transforms raw AST lists into a relational, queryable graph structure."""
    
    @staticmethod
    def build_module_map(ast_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Maps out the structural footprint of the entire repository."""
        module_graph = {}
        
        for filename, data in ast_metadata.items():
            if not data.get("syntax_valid"):
                continue
                
            module_graph[filename] = {
                "total_classes": len(data.get("classes", [])),
                "total_functions": len(data.get("functions", [])),
                "exposed_entities": [f["name"] for f in data.get("functions", [])]
            }
            
        logger.debug(f"ASTGraphBuilder mapped {len(module_graph)} valid modules.")
        return module_graph