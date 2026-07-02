from typing import Dict, Any, List
from orchestrator.state import AgentState
from core.llm.ollama_client import ollama_ai
from utils.logger import logger

class TutorAgent:
    def __init__(self):
        self.system_prompt = (
            "You are a Senior Staff Software Engineer and Mentor. "
            "Your goal is to explain complex architectural flaws, security risks, and performance bottlenecks "
            "to a developer. Tailor your response based on whether the issue is new or persistent. "
            "Return a JSON object containing a 'summary' and an array of 'actionable_patches'."
        )

    def _prioritize_issues(self, state: AgentState) -> List[Dict[str, Any]]:
        """
        Sorts and filters issues to prevent token exhaustion.
        Prioritizes CRITICAL severity, then HIGH, then Regressions (new issues).
        """
        all_issues = state.get("performance_bottlenecks", []) + state.get("security_vulnerabilities", [])
        
        if not all_issues:
            return []

        # Sort logic: Severity first, then novelty
        severity_weight = {"CRITICAL": 3, "HIGH": 2, "MEDIUM": 1, "LOW": 0}
        
        sorted_issues = sorted(
            all_issues,
            key=lambda x: (
                severity_weight.get(x.get("severity", "LOW").upper(), 0),
                1 if x.get("is_new", True) else 0
            ),
            reverse=True
        )
        
        # Take the top 3 most critical issues to explain in-depth
        return sorted_issues[:3]

    def _build_tutor_prompt(self, priority_issues: List[Dict[str, Any]]) -> str:
        """Constructs a context-aware prompt based on the Memory Agent's findings."""
        prompt_parts = ["Analyze the following critical system issues and provide educational guidance:\n"]
        
        for issue in priority_issues:
            times_seen = issue.get("times_seen", 1)
            file_ref = issue.get("file", "Unknown Module")
            desc = issue.get("issue", issue.get("risk", "Unknown Issue"))
            
            prompt_parts.append(f"- Location: {file_ref}")
            prompt_parts.append(f"  Issue: {desc}")
            
            # Adaptive Tone Logic
            if times_seen > 3:
                prompt_parts.append(f"  Context: The developer has failed to fix this {times_seen} times. Provide a DIRECT CODE PATCH and skip the introductory theory.")
            elif not issue.get("is_new"):
                prompt_parts.append(f"  Context: This is an existing issue (seen {times_seen} times). Provide a strong hint on how to refactor this.")
            else:
                prompt_parts.append("  Context: Brand new regression. Explain WHY this is bad practice gently.")
                
        prompt_parts.append("\nReturn a JSON dict exactly like this:")
        prompt_parts.append('{"executive_summary": "string", "actionable_patches": [{"file": "string", "explanation": "string", "code_snippet": "string"}]}')
        
        return "\n".join(prompt_parts)

    async def execute_analysis(self, state: AgentState) -> Dict[str, Any]:
        """
        Synthesizes all pipeline logs into the Final Intelligence Report.
        """
        logger.info("Tutor Agent initializing. Synthesizing Final Intelligence Report...")
        
        priority_issues = self._prioritize_issues(state)
        
        if not priority_issues:
            logger.info("No critical issues found. Generating clean health report.")
            final_report = {
                "executive_summary": "System logic and architecture are sound. No critical vulnerabilities or bottlenecks detected.",
                "actionable_patches": [],
                "system_health": "OPTIMAL"
            }
            return {
                "final_intelligence_report": final_report,
                "current_agent": "TutorAgent",
                "execution_status": "COMPLETED",
                "logs": ["Tutor Agent generated optimal health report."]
            }

        prompt = self._build_tutor_prompt(priority_issues)
        
        # Query LLM for the educational synthesis
        llm_feedback = await ollama_ai.generate_structured_response(
            prompt=prompt, 
            system_prompt=self.system_prompt
        )

        final_report = {
            "executive_summary": llm_feedback.get("executive_summary", "Review the localized issues below."),
            "actionable_patches": llm_feedback.get("actionable_patches", []),
            "system_health": "NEEDS_ATTENTION",
            "historical_notes": state.get("historical_context", [])
        }

        logger.info("Tutor Agent synthesis complete.")

        return {
            "final_intelligence_report": final_report,
            "current_agent": "TutorAgent",
            "execution_status": "COMPLETED",
            "logs": ["Tutor Agent compiled Final Intelligence Report with actionable code patches."]
        }

# Expose singleton for the LangGraph workflow
tutor_agent_instance = TutorAgent()