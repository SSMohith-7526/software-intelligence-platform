from typing import Dict, Any, List
from orchestrator.workflow import compiled_ai_os_pipeline
from core.shared_context.context_manager import global_context
from utils.logger import logger

class AIOrchestrator:
    """Facade for managing LangGraph execution lifecycles."""
    
    def _build_initial_state(self, repository_path: str, files: Dict[str, str]) -> Dict[str, Any]:
        """Constructs the baseline state required by the Context Bus."""
        return {
            "repository_path": repository_path,
            "target_files": list(files.keys()),
            "file_contents": files,
            "ast_metadata": {},
            "control_flow_graphs": {},
            "security_vulnerabilities": [],
            "performance_bottlenecks": [],
            "runtime_simulation_logs": {},
            "historical_context": [],
            "tutor_explanations": [],
            "final_intelligence_report": {},
            "current_agent": "Initializing",
            "execution_status": "PENDING",
            "logs": ["Orchestrator initialized new execution state."]
        }

    async def run_full_pipeline(self, repository_path: str, files: Dict[str, str]) -> Dict[str, Any]:
        """
        Executes the entire pipeline synchronously and returns the final state.
        Used primarily by REST API routes rather than WebSockets.
        """
        logger.info(f"Orchestrator beginning full pipeline execution for {repository_path}")
        
        # Clear out-of-band memory from previous runs
        global_context.clear_context()
        
        state = self._build_initial_state(repository_path, files)
        final_state = None
        
        try:
            # .ainvoke() runs the graph to completion in one shot
            final_state = await compiled_ai_os_pipeline.ainvoke(state)
            logger.info("Orchestrator successfully completed full pipeline execution.")
            return final_state.get("final_intelligence_report", {})
            
        except Exception as e:
            logger.error(f"Orchestrator pipeline failed fatally: {str(e)}")
            raise RuntimeError(f"Pipeline execution failed: {str(e)}")

# Expose a generic instance
orchestrator_engine = AIOrchestrator()