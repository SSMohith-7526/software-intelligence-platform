import psutil
from fastapi import APIRouter, status
from typing import Dict, Any
from core.llm.ollama_client import ollama_ai
from utils.logger import logger

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
async def system_health_check() -> Dict[str, Any]:
    """Deep system diagnostic check."""
    
    # 1. Check OS Memory constraints
    ram = psutil.virtual_memory()
    memory_status = "CRITICAL" if ram.percent > 90 else "OPTIMAL"

    # 2. Ping Local LLM (Ollama)
    # We send a tiny, fast prompt to ensure the model is loaded in VRAM
    llm_ping = await ollama_ai.generate_structured_response(
        prompt="Reply with exactly: {'status': 'active'}",
        system_prompt="You are a ping responder."
    )
    llm_status = "ONLINE" if "status" in llm_ping or "error" not in llm_ping else "OFFLINE"

    health_report = {
        "status": "OPERATIONAL" if llm_status == "ONLINE" and memory_status == "OPTIMAL" else "DEGRADED",
        "system_resources": {
            "cpu_usage_percent": psutil.cpu_percent(),
            "ram_usage_percent": ram.percent,
            "ram_status": memory_status
        },
        "llm_engine": {
            "provider": "Ollama",
            "status": llm_status,
            "target_model": ollama_ai.default_model
        }
    }
    
    logger.debug(f"Health check executed. System status: {health_report['status']}")
    return health_report