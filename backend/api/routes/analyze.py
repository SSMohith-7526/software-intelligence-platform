from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
from orchestrator.orchestrator import AIOrchestrator
from utils.logger import logger

router = APIRouter()
orchestrator_engine = AIOrchestrator()

@router.post("/analyze/sync", status_code=status.HTTP_200_OK)
async def synchronous_analysis(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Standard REST endpoint for analysis. Blocks until the LangGraph pipeline finishes.
    Ideal for CI/CD integration or small file analysis.
    """
    repository_path = payload.get("repository_path", "api_upload")
    files = payload.get("files", {})

    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No 'files' dictionary provided in payload."
        )

    logger.info(f"REST API triggered synchronous analysis for {len(files)} files.")
    
    try:
        # Execute the pipeline and wait for the final state
        final_report = await orchestrator_engine.run_full_pipeline(repository_path, files)
        return {
            "status": "success",
            "report": final_report
        }
    except Exception as e:
        logger.error(f"Synchronous pipeline failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Engine failure: {str(e)}"
        )