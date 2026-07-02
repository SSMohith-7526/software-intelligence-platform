import os
import json
import hashlib
from typing import Dict, Any, List
from orchestrator.state import AgentState
from utils.logger import logger

class MemoryAgent:
    def __init__(self, history_file: str = ".ai_os_memory.json"):
        self.history_file = history_file
        # In a production environment, this would be a Vector DB (Chroma/Pinecone) or Redis.
        # For tomorrow's prototype, a local JSON ledger guarantees persistence without Docker overhead.

    def _generate_issue_hash(self, issue: Dict[str, Any]) -> str:
        """
        Creates a deterministic SHA-256 hash based on the core traits of an issue.
        This prevents the system from spamming the user with duplicate alerts.
        """
        # Extract deterministic fields, ignoring dynamic ones like timestamps
        core_string = f"{issue.get('file', '')}:{issue.get('function', '')}:{issue.get('issue', issue.get('risk', ''))}"
        return hashlib.sha256(core_string.encode('utf-8')).hexdigest()

    def _load_history(self) -> Dict[str, Any]:
        """Loads the historical ledger of known codebase issues."""
        if not os.path.exists(self.history_file):
            return {"known_issues": {}, "resolved_issues": []}
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error("Memory ledger corrupted. Initializing fresh memory state.")
            return {"known_issues": {}, "resolved_issues": []}

    def _save_history(self, history_data: Dict[str, Any]) -> None:
        """Persists the updated ledger to disk."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to persist memory state: {str(e)}")

    async def execute_analysis(self, state: AgentState) -> Dict[str, Any]:
        """
        Cross-references newly discovered issues against the historical ledger.
        """
        logger.info("Memory Agent initializing. Cross-referencing current state with historical ledger...")
        
        history = self._load_history()
        known_issues = history.get("known_issues", {})
        
        current_bottlenecks = state.get("performance_bottlenecks", [])
        current_vulnerabilities = state.get("security_vulnerabilities", [])
        
        all_current_issues = current_bottlenecks + current_vulnerabilities
        current_issue_hashes = set()
        
        annotated_historical_context = []

        # 1. Process current issues and check for duplicates
        for issue in all_current_issues:
            issue_hash = self._generate_issue_hash(issue)
            current_issue_hashes.add(issue_hash)
            
            if issue_hash in known_issues:
                # Issue already exists in memory
                known_issues[issue_hash]["times_seen"] += 1
                issue["is_new"] = False
                issue["times_seen"] = known_issues[issue_hash]["times_seen"]
            else:
                # Brand new issue detected (Regression)
                known_issues[issue_hash] = {
                    "data": issue,
                    "times_seen": 1,
                    "status": "active"
                }
                issue["is_new"] = True
                issue["times_seen"] = 1
                annotated_historical_context.append(f"REGRESSION DETECTED: {issue.get('issue', issue.get('risk', 'Unknown'))}")

        # 2. Check for resolved issues (in memory, but not in current run)
        resolved_count = 0
        for stored_hash, stored_data in list(known_issues.items()):
            if stored_hash not in current_issue_hashes and stored_data["status"] == "active":
                stored_data["status"] = "resolved"
                annotated_historical_context.append(f"RESOLVED: {stored_data['data'].get('issue', stored_data['data'].get('risk', ''))}")
                resolved_count += 1

        # 3. Persist the updated state back to disk
        history["known_issues"] = known_issues
        self._save_history(history)

        logger.info(f"Memory Agent complete. Tracked {len(all_current_issues)} active issues. {resolved_count} issues marked as resolved.")

        return {
            "historical_context": annotated_historical_context,
            "current_agent": "MemoryAgent",
            "execution_status": "COMPLETED",
            "logs": [f"Memory Agent cross-referenced ledger. Found {len([i for i in all_current_issues if i.get('is_new')])} new regressions."]
        }

# Expose singleton for the LangGraph workflow
memory_agent_instance = MemoryAgent()