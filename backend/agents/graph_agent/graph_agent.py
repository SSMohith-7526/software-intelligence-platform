from typing import Dict, Any, List, Set
from orchestrator.state import AgentState
from utils.logger import logger

class GraphAgent:
    def __init__(self):
        # We process internal modules, filtering out standard library 
        # noise to focus on the developer's actual architecture.
        pass

    def _detect_cycles(self, dependency_graph: Dict[str, List[str]]) -> List[List[str]]:
        """
        Uses a deep-first search (DFS) with a coloring algorithm (White, Gray, Black) 
        to detect circular dependencies (e.g., A imports B, B imports A).
        """
        visited = set()
        path = []
        cycles = []

        def dfs(node: str):
            if node in path:
                # Cycle detected: slice the path from the first occurrence of the node
                cycle_start_index = path.index(node)
                cycles.append(path[cycle_start_index:] + [node])
                return
            if node in visited:
                return

            visited.add(node)
            path.append(node)

            # Traverse neighbors (only looking at internal standard dependencies for cycles)
            neighbors = dependency_graph.get(node, {}).get("standard", [])
            for neighbor in neighbors:
                # Only traverse if the neighbor is actually a file in our graph
                # (prevents traversing out into external pip packages)
                if any(neighbor in known_node for known_node in dependency_graph.keys()):
                    # Find the exact node key that matches the neighbor module name
                    matched_node = next((k for k in dependency_graph.keys() if neighbor in k), None)
                    if matched_node:
                        dfs(matched_node)

            path.pop()

        for current_node in dependency_graph.keys():
            dfs(current_node)

        # Deduplicate cycles (since A->B->A is the same as B->A->B)
        unique_cycles = []
        seen_cycle_sets = []
        for cycle in cycles:
            cycle_set = set(cycle)
            if cycle_set not in seen_cycle_sets:
                seen_cycle_sets.append(cycle_set)
                unique_cycles.append(cycle)

        return unique_cycles

    def _calculate_module_criticality(self, dependency_graph: Dict[str, Dict[str, List[str]]]) -> Dict[str, int]:
        """
        Calculates the 'In-Degree' of each module. 
        If a module is imported by 15 other files, it has a high blast radius.
        """
        in_degrees = {node: 0 for node in dependency_graph.keys()}
        
        for node, deps in dependency_graph.items():
            for imported_module in deps.get("standard", []):
                # Map the import string back to a physical file in our graph
                for target_node in in_degrees.keys():
                    if imported_module in target_node:
                        in_degrees[target_node] += 1
                        break
                        
        # Sort by most critical (highest in-degree) descending
        return dict(sorted(in_degrees.items(), key=lambda item: item[1], reverse=True))

    async def execute_analysis(self, state: AgentState) -> Dict[str, Any]:
        """
        Transforms raw dependencies into a queryable topological graph.
        """
        logger.info("Graph Agent initializing topological mapping...")
        
        # Retrieve the dependency map injected by the Repository Agent
        ast_meta = state.get("ast_metadata", {})
        dependency_graph = ast_meta.get("dependency_graph", {})
        
        if not dependency_graph:
            logger.warning("No dependency graph found in state. Graph Agent bypassing.")
            return {
                "current_agent": "GraphAgent",
                "execution_status": "SKIPPED",
                "logs": ["Graph Agent skipped: No dependency data available."]
            }

        # 1. Detect Architectural Flaws (Cycles)
        circular_dependencies = self._detect_cycles(dependency_graph)
        if circular_dependencies:
            logger.warning(f"Detected {len(circular_dependencies)} circular dependencies!")

        # 2. Map Module Criticality (Blast Radius)
        criticality_map = self._calculate_module_criticality(dependency_graph)

        # 3. Format the Graph State for Downstream Agents
        control_flow_graphs = {
            "criticality_ranking": criticality_map,
            "circular_dependencies": circular_dependencies,
            "total_edges": sum(len(d.get("standard", [])) for d in dependency_graph.values())
        }

        # If cycles are found, we flag this as a critical architectural flaw for the Context Bus
        performance_flags = []
        if circular_dependencies:
            for cycle in circular_dependencies:
                performance_flags.append({
                    "category": "Architecture",
                    "severity": "CRITICAL",
                    "details": f"Circular dependency detected: {' -> '.join(cycle)}. This causes memory leaks and fragile testing."
                })

        logger.info("Graph Agent completed topological mapping.")

        return {
            "control_flow_graphs": control_flow_graphs,
            "performance_bottlenecks": performance_flags, # Appends using operator.add in State
            "current_agent": "GraphAgent",
            "execution_status": "COMPLETED",
            "logs": [f"Graph Agent built topology map. Found {len(circular_dependencies)} cycles."]
        }

# Singleton instance
graph_agent_instance = GraphAgent()