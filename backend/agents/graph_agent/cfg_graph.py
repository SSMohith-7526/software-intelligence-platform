from typing import Dict, Any
from utils.logger import logger

class CFGBuilder:
    """Models logical branching and execution paths within modules."""
    
    @staticmethod
    def estimate_complexity(ast_metadata: Dict[str, Any]) -> Dict[str, str]:
        """
        Provides a baseline complexity estimation to help the downstream 
        Runtime Agent prioritize which files to simulate.
        """
        complexity_map = {}
        
        for filename, data in ast_metadata.items():
            func_count = len(data.get("functions", []))
            class_count = len(data.get("classes", []))
            
            # Heuristic: Files with many functions/classes have higher branching potential
            total_structures = func_count + class_count
            
            if total_structures > 20:
                complexity_map[filename] = "HIGH"
            elif total_structures > 10:
                complexity_map[filename] = "MEDIUM"
            else:
                complexity_map[filename] = "LOW"
                
        return complexity_map