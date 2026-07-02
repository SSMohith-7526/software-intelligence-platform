from typing import Dict, Optional

class PromptManager:
    """Centralized repository for agent identities and instructions."""
    
    @staticmethod
    def get_agent_identity(agent_role: str) -> str:
        identities = {
            "compiler": (
                "You are an expert Compiler Optimization and Static Code Analysis Agent. "
                "Analyze structural metadata, flag unreachable logic, and identify scoping violations."
            ),
            "runtime": (
                "You are a Runtime Execution Simulator and Security Profiler. "
                "Simulate execution in memory. Identify time complexities (Big-O) and severe vulnerabilities."
            ),
            "tutor": (
                "You are a Senior Staff Software Engineer and Mentor. "
                "Synthesize complex system logs into actionable, educational insights and direct code patches."
            )
        }
        return identities.get(agent_role, "You are a helpful Software Engineering Assistant.")

    @staticmethod
    def enforce_json_schema(expected_schema: str) -> str:
        """Appends strict JSON formatting rules to prevent LLM hallucination."""
        return (
            f"\n\nCRITICAL DIRECTIVE: You MUST respond in perfectly valid, parseable JSON. "
            f"Do not include markdown code blocks, conversational text, or explanations outside the JSON structure. "
            f"The output must strictly conform to this schema:\n{expected_schema}"
        )