import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from orchestrator.state import AgentState
from orchestrator.workflow import compiled_ai_os_pipeline
from utils.logger import logger
from api.routes import upload

app = FastAPI(title="Software Engineering Agentic AI OS Runtime", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect the REST endpoint for file ingestion
app.include_router(upload.router)

@app.get("/api/health")
async def basic_health_check():
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
        
        # Execute LangGraph and stream node transitions to React
        async for output in compiled_ai_os_pipeline.astream(initial_state):
            for node_name, state_update in output.items():
                await websocket.send_text(json.dumps(state_update))
                
    except WebSocketDisconnect:
        logger.info("Dashboard WebSocket disconnected.")
    except Exception as e:
        logger.error(f"Pipeline execution fault: {str(e)}")
        await websocket.send_text(json.dumps({
            "execution_status": "ERROR", 
            "logs": [f"CRITICAL FAULT: {str(e)}"]
        }))