import ast
from typing import Dict, Any, List
from orchestrator.state import AgentState
from core.llm.ollama_client import ollama_ai
from utils.logger import logger

class CompilerAgent:
    def __init__(self):
        self.system_prompt = (
            "You are an expert Compiler Optimization and Static Code Analysis Agent. "
            "Analyze the provided AST metadata structure for semantic structural defects, "
            "unreachable branch configurations, and scoping violations. Return raw JSON matching "
            "the requested format perfectly."
        )

    def extract_native_ast(self, code_content: str, filename: str) -> Dict[str, Any]:
        """Uses Python's compiler subsystem to build a precise Abstract Syntax Tree summary."""
        try:
            parsed_tree = ast.parse(code_content, filename=filename)
            
            summary = {
                "functions": [],
                "classes": [],
                "imports": [],
                "syntax_valid": True
            }
            
            for node in ast.walk(parsed_tree):
                if isinstance(node, ast.FunctionDef):
                    args = [arg.arg for arg in node.args.args]
                    summary["functions"].append({"name": node.name, "args": args, "line": node.lineno})
                elif isinstance(node, ast.ClassDef):
                    summary["classes"].append({"name": node.name, "line": node.lineno})
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    summary["imports"].append(ast.unparse(node))
            return summary
            
        except SyntaxError as e:
            logger.warning(f"Syntax validation failed during compilation processing for {filename}: {e.msg}")
            return {
                "syntax_valid": False,
                "error_message": e.msg,
                "line_number": e.lineno,
                "offset": e.offset
            }

    async def execute_analysis(self, state: AgentState) -> Dict[str, Any]:
        """Orchestration node execution point."""
        logger.info("Compiler Agent processing state context bus maps...")
        compiled_ast_registry = {}
        structural_errors = []
        
        for filename, content in state.get("file_contents", {}).items():
            ast_data = self.extract_native_ast(content, filename)
            compiled_ast_registry[filename] = ast_data
            if not ast_data["syntax_valid"]:
                structural_errors.append(f"Syntax error in {filename} at line {ast_data.get('line_number')}: {ast_data.get('error_message')}")

        # Construct semantic review prompt
        prompt = (
            f"Analyze the following compiled module AST tree summaries:\n"
            f"{ast.unparse(ast.parse(str(compiled_ast_registry)))}\n\n"
            f"Identify code logic violations. Return a JSON dictionary formatted exactly as:\n"
            f'{{"architectural_flaws": [{"file": "name", "issue": "description", "severity": "CRITICAL|WARNING"}]}}'
        )
        
        llm_feedback = await ollama_ai.generate_structured_response(
            prompt=prompt, 
            system_prompt=self.system_prompt
        )

        return {
            "ast_metadata": compiled_ast_registry,
            "current_agent": "CompilerAgent",
            "execution_status": "COMPLETED",
            "logs": [f"Successfully compiled and parsed {len(compiled_ast_registry)} module boundaries."],
            "performance_bottlenecks": [{"category": "Compilation", "details": err} for err in structural_errors]
        }

# Expose singleton for the LangGraph workflow
compiler_agent_instance = CompilerAgent()