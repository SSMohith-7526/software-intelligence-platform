from typing import Dict, Any, List
from utils.logger import logger

class ExecutionSimulator:
    """
    Safely mimics code execution paths by analyzing the CFG and AST metadata
    prior to sending it to the LLM for deep time-complexity analysis.
    """
    
    @staticmethod
    def prepare_sandbox_payload(file_contents: Dict[str, str], criticality_map: Dict[str, int]) -> Dict[str, str]:
        """
        Filters the raw code down to ONLY the most critical execution paths.
        This prevents blowing out the LLM token window with dead code.
        """
        sandbox_payload = {}
        
        # Sort files by criticality (blast radius) descending
        sorted_files = sorted(criticality_map.items(), key=lambda item: item[1], reverse=True)
        
        # Only simulate the top 3 most critical modules
        top_targets = [f[0] for f in sorted_files[:3]]
        
        for target in top_targets:
            if target in file_contents:
                # We truncate massive files to 1500 lines to prevent memory overflow in the simulator
                lines = file_contents[target].split('\n')
                sandbox_payload[target] = '\n'.join(lines[:1500])
                
        logger.debug(f"ExecutionSimulator prepared {len(sandbox_payload)} critical modules for runtime evaluation.")
        return sandbox_payload