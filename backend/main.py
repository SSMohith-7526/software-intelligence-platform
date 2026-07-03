import json
import warnings
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from orchestrator.state import AgentState
from orchestrator.workflow import compiled_ai_os_pipeline
from utils.logger import logger

# 1. Include route endpoints from your api/routes module
from api.routes import upload, health, analyze

# 2. Suppress benign third-party deprecation warnings (e.g., LangChain/LangGraph)
warnings.filterwarnings("ignore", category=UserWarning, module="langgraph")
warnings.filterwarnings("ignore", category=DeprecationWarning)

app = FastAPI(
    title="Software Engineering Agentic AI OS Runtime", 
    version="1.0.0",
    description="Engine core managing graph state transitions for multi-agent code analysis."
)

# 3. Configure CORS policies for seamless React frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Connect the modular REST endpoints
app.include_router(upload.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(analyze.router, prefix="/api")

@app.get("/")
async def root_heartbeat():
    """
    Landing endpoint to check API status and prevent 404 browser errors.
    """
    return {
        "status": "ONLINE",
        "system": "Software Intelligence Platform Engine Core",
        "documentation": "/docs",
        "websocket_channel": "/api/ws/analyze"
    }

@app.get("/api/health")
async def basic_health_check():
    """Fallback inline endpoint for monitoring service status."""
    return {"status": "online", "engine": "LangGraph state pipeline fully operational"}

@app.websocket("/api/ws/analyze")
async def websocket_analysis_endpoint(websocket: WebSocket):
    """
    Handles real-time payload streaming of graph state changes back to dashboard components.
    """
    await websocket.accept()
    logger.info("Real-time reactive UI pipeline socket attached successfully.")
    
    try:
        # Receive analysis request payload parameters from user dashboard frontend
        raw_data = await websocket.receive_text()
        payload = json.loads(raw_data)
        
        # Form initial state bus baseline context dictionary structure
        initial_state = {
            "repository_path": payload.get("repository_path", "sandbox_root"),
            "target_files": list(payload.get("files", {}).keys()),
            "file_contents": payload.get("files", {}),
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
            "logs": ["Booting LangGraph pipeline..."]
        }
        
        # Execute LangGraph and stream node transitions asynchronously to the React client
        async for output in compiled_ai_os_pipeline.astream(initial_state):
            for node_name, state_update in output.items():
                # Force update fields to propagate downstream if missing
                if "current_agent" not in state_update:
                    state_update["current_agent"] = node_name
                
                await websocket.send_text(json.dumps(state_update))
                
    except WebSocketDisconnect:
        logger.info("Dashboard WebSocket connection cleanly terminated.")
    except Exception as e:
        logger.error(f"Pipeline execution fault encountered: {str(e)}")
        try:
            await websocket.send_text(json.dumps({
                "execution_status": "ERROR", 
                "logs": [f"CRITICAL ENGINE FAULT: {str(e)}"]
            }))
        except Exception:
            pass  # Socket might already be closed

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
