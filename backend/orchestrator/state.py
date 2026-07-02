from typing import Dict, Any, List, TypedDict, Annotated
import operator

class AgentState(TypedDict):
    repository_path: str
    target_files: List[str]
    file_contents: Dict[str, str]
    ast_metadata: Dict[str, Any]
    control_flow_graphs: Dict[str, Any]
    security_vulnerabilities: Annotated[List[Dict[str, Any]], operator.add]
    performance_bottlenecks: Annotated[List[Dict[str, Any]], operator.add]
    runtime_simulation_logs: Dict[str, Any]
    historical_context: List[str]
    tutor_explanations: List[str]
    final_intelligence_report: Dict[str, Any]
    current_agent: str
    execution_status: str
    logs: Annotated[List[str], operator.add]