from typing import Dict, Any
from langgraph.graph import StateGraph, END
from orchestrator.state import AgentState

# Import all Agent Classes
from agents.repository_agent.repository_agent import RepositoryAgent
from agents.graph_agent.graph_agent import GraphAgent
from agents.compiler_agent.compiler_agent import CompilerAgent
from agents.runtime_agent.runtime_agent import RuntimeAgent
from agents.memory_agent.memory_agent import MemoryAgent
from agents.tutor_agent.tutor_agent import TutorAgent

from utils.logger import logger

# 1. Instantiate the Agents
repo_agent = RepositoryAgent()
graph_agent = GraphAgent()
compiler_agent = CompilerAgent()
runtime_agent = RuntimeAgent()
memory_agent = MemoryAgent()
tutor_agent = TutorAgent()

# 2. Define Node Wrapper Functions for LangGraph
async def run_repo_node(state: AgentState) -> Dict[str, Any]:
    return await repo_agent.execute_analysis(state)

async def run_graph_node(state: AgentState) -> Dict[str, Any]:
    return await graph_agent.execute_analysis(state)

async def run_compiler_node(state: AgentState) -> Dict[str, Any]:
    return await compiler_agent.execute_analysis(state)

async def run_runtime_node(state: AgentState) -> Dict[str, Any]:
    return await runtime_agent.execute_analysis(state)

async def run_memory_node(state: AgentState) -> Dict[str, Any]:
    return await memory_agent.execute_analysis(state)

async def run_tutor_node(state: AgentState) -> Dict[str, Any]:
    return await tutor_agent.execute_analysis(state)

def construct_agentic_workflow() -> StateGraph:
    """Builds the reactive execution pipeline mapping every OS module."""
    workflow_graph = StateGraph(AgentState)
    
    # Add all processing nodes to the graph
    workflow_graph.add_node("RepositoryAgent", run_repo_node)
    workflow_graph.add_node("GraphAgent", run_graph_node)
    workflow_graph.add_node("CompilerAgent", run_compiler_node)
    workflow_graph.add_node("RuntimeAgent", run_runtime_node)
    workflow_graph.add_node("MemoryAgent", run_memory_node)
    workflow_graph.add_node("TutorAgent", run_tutor_node)
    
    # Establish Entry Point
    workflow_graph.set_entry_point("RepositoryAgent")
    
    # Establish the linear pipeline transitions
    workflow_graph.add_edge("RepositoryAgent", "GraphAgent")
    workflow_graph.add_edge("GraphAgent", "CompilerAgent")
    workflow_graph.add_edge("CompilerAgent", "RuntimeAgent")
    workflow_graph.add_edge("RuntimeAgent", "MemoryAgent")
    workflow_graph.add_edge("MemoryAgent", "TutorAgent")
    
    # Terminate after Intelligence Synthesis
    workflow_graph.add_edge("TutorAgent", END)
    
    return workflow_graph.compile()

# Master Executable Reference (This is what main.py was looking for!)
compiled_ai_os_pipeline = construct_agentic_workflow()