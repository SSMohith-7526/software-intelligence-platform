from typing import Dict, Any, List
from utils.logger import logger

class HeapTracker:
    """Analyzes simulated runtime data for un-garbage-collected allocations."""
    
    @staticmethod
    def detect_leaks(runtime_bottlenecks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filters the runtime logs specifically for memory-bound issues."""
        heap_issues = []
        
        leak_keywords = ["unclosed", "leak", "memory", "allocation", "garbage collection"]
        
        for issue in runtime_bottlenecks:
            description = issue.get("issue", "").lower()
            if any(keyword in description for keyword in leak_keywords):
                heap_issues.append({
                    "file": issue.get("file"),
                    "risk": "Heap Memory Leak Detected",
                    "details": issue.get("issue")
                })
                
        return heap_issues