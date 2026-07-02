from typing import Dict, Any, List
from orchestrator.state import AgentState
from core.llm.ollama_client import ollama_ai
from utils.logger import logger

class RuntimeAgent:
    def __init__(self):
        self.system_prompt = (
            "You are a highly advanced Runtime Execution Simulator and Security Profiler. "
            "Your job is to read parsed Abstract Syntax Trees (AST) and Control Flow Graphs (CFG), "
            "and simulate their execution in memory. "
            "Identify O(n^2) or worse time complexities, potential memory leaks (e.g., unclosed file handlers), "
            "and severe security vulnerabilities (e.g., SQL injection, arbitrary code execution). "
            "Respond ONLY in valid JSON format matching the requested schema."
        )

    def _prepare_simulation_payload(self, state: AgentState) -> Dict[str, Any]:
        """
        Extracts only the high-risk functions and critical modules identified by the 
        Graph Agent to save LLM context window limits and processing time.
        """
        ast_data = state.get("ast_metadata", {})
        critical_modules = state.get("control_flow_graphs", {}).get("criticality_ranking", {})
        
        # If we have a criticality ranking, we only simulate the top 5 most imported modules
        # to prevent overloading the local LLM with massive payloads.
        target_files = list(critical_modules.keys())[:5] if critical_modules else list(ast_data.keys())[:5]
        
        simulation_payload = {}
        for file in target_files:
            if file in ast_data:
                # Strip out imports, only send functions and classes for runtime simulation
                simulation_payload[file] = {
                    "functions": ast_data[file].get("functions", []),
                    "classes": ast_data[file].get("classes", [])
                }
                
        return simulation_payload

    async def execute_analysis(self, state: AgentState) -> Dict[str, Any]:
        """
        Orchestrates the simulated runtime environment and logs performance bottlenecks.
        """
        logger.info("Runtime Agent initializing execution simulation...")
        
        simulation_payload = self._prepare_simulation_payload(state)
        
        if not simulation_payload:
            logger.warning("No valid AST logic found for Runtime Agent to simulate.")
            return {
                "current_agent": "RuntimeAgent",
                "execution_status": "SKIPPED",
                "logs": ["Runtime simulation skipped: No executable logic structures found."]
            }

        # Construct the strict JSON prompt
        prompt = (
            f"Simulate the execution of the following module structures:\n"
            f"{simulation_payload}\n\n"
            f"Analyze for runtime complexities and security vulnerabilities. "
            f"Return a JSON dictionary formatted exactly as:\n"
            f'{{\n'
            f'  "performance_bottlenecks": [{{"file": "string", "function": "string", "issue": "description", "complexity": "O(N...)"}}],\n'
            f'  "security_vulnerabilities": [{{"file": "string", "risk": "description", "severity": "HIGH|MEDIUM|LOW"}}]\n'
            f'}}'
        )
        
        # Execute the LLM simulation via our resilient Ollama client
        llm_feedback = await ollama_ai.generate_structured_response(
            prompt=prompt, 
            system_prompt=self.system_prompt
        )

        # Extract the specific arrays, defaulting to empty lists if the LLM hallucinated the schema
        new_bottlenecks = llm_feedback.get("performance_bottlenecks", [])
        new_vulnerabilities = llm_feedback.get("security_vulnerabilities", [])

        total_issues = len(new_bottlenecks) + len(new_vulnerabilities)
        logger.info(f"Runtime simulation complete. Identified {total_issues} potential runtime issues.")

        return {
            # These lists will be appended to the global state using operator.add in state.py
            "performance_bottlenecks": new_bottlenecks,
            "security_vulnerabilities": new_vulnerabilities,
            "runtime_simulation_logs": {"simulated_modules": list(simulation_payload.keys())},
            "current_agent": "RuntimeAgent",
            "execution_status": "COMPLETED",
            "logs": [f"Runtime Agent simulated execution for {len(simulation_payload)} modules. Found {total_issues} issues."]
        }

# Expose singleton for the LangGraph workflow
runtime_agent_instance = RuntimeAgent()