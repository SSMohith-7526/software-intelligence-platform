import os
import ast
from typing import Dict, Any, List, Set, Tuple
from orchestrator.state import AgentState
from utils.logger import logger

class RepositoryAgent:
    def __init__(self):
        # Prevent the agent from getting stuck in massive or irrelevant directories
        self.ignore_dirs = {
            '.git', 'node_modules', '__pycache__', 'venv', 'env', 
            '.venv', 'dist', 'build', '.idea', '.vscode', 'coverage'
        }
        # Prevent reading binary or media files into string memory
        self.ignore_exts = {
            '.pyc', '.png', '.jpg', '.jpeg', '.gif', '.pdf', '.exe', 
            '.dll', '.so', '.zip', '.tar', '.gz', '.mp4', '.sqlite3'
        }
        # Fallback encodings for robust file reading
        self.encodings = ['utf-8', 'latin-1', 'cp1252']

    def _safe_read_file(self, filepath: str) -> str:
        """Attempts to read a file using multiple encodings to prevent crashes on bad characters."""
        for encoding in self.encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.error(f"Failed to read {filepath} due to OS/Permission error: {str(e)}")
                return ""
        logger.warning(f"Could not decode {filepath} with any standard encoding. Skipping content.")
        return ""

    def _extract_dependencies(self, file_content: str, filepath: str) -> Dict[str, List[str]]:
        """
        Uses Python's AST to reliably extract import statements.
        This builds the foundation for the Knowledge Graph agent later.
        """
        deps = {"standard": [], "internal": [], "third_party": []}
        
        if not filepath.endswith('.py'):
            return deps # Only parse Python files for AST dependencies

        try:
            tree = ast.parse(file_content, filename=filepath)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        deps["standard"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module if node.module else "relative_import"
                    deps["standard"].append(module)
        except SyntaxError:
            # We don't crash here; the Compiler Agent handles Syntax Errors.
            # We just log it and move on with empty dependencies for this file.
            logger.debug(f"Syntax error while mapping dependencies in {filepath}. Deferring to Compiler Agent.")
            
        return deps

    def scan_repository(self, root_path: str) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """
        Walks the directory structure, avoiding blacklisted folders and files.
        Returns the raw contents and the dependency map.
        """
        file_contents = {}
        dependency_map = {}

        if not os.path.exists(root_path):
            logger.error(f"Target repository path does not exist: {root_path}")
            return file_contents, dependency_map

        for dirpath, dirnames, filenames in os.walk(root_path):
            # Mutate dirnames in-place to prevent os.walk from entering ignored directories
            dirnames[:] = [d for d in dirnames if d not in self.ignore_dirs]

            for filename in filenames:
                ext = os.path.splitext(filename)[1].lower()
                if ext in self.ignore_exts:
                    continue

                full_path = os.path.join(dirpath, filename)
                
                # Normalize path for cross-OS compatibility (Windows \ vs Linux /)
                relative_path = os.path.relpath(full_path, root_path).replace("\\", "/")
                
                content = self._safe_read_file(full_path)
                if content:
                    file_contents[relative_path] = content
                    dependency_map[relative_path] = self._extract_dependencies(content, relative_path)

        return file_contents, dependency_map

    async def execute_analysis(self, state: AgentState) -> Dict[str, Any]:
        """
        The main entry point for the LangGraph orchestrator.
        Takes the state, maps the repository, and updates the shared Context Bus.
        """
        logger.info("Repository Agent initialized. Scanning target environment...")
        
        target_path = state.get("repository_path", ".")
        
        # If the user uploaded specific files via UI instead of a path, use those.
        existing_files = state.get("file_contents", {})
        
        if existing_files:
            logger.info("Processing files provided directly from UI upload payload.")
            file_contents = existing_files
            dependency_map = {
                path: self._extract_dependencies(content, path) 
                for path, content in file_contents.items()
            }
        else:
            logger.info(f"Scanning local filesystem at path: {target_path}")
            file_contents, dependency_map = self.scan_repository(target_path)

        total_files = len(file_contents)
        logger.info(f"Repository Agent finished. Ingested {total_files} files.")

        return {
            "target_files": list(file_contents.keys()),
            "file_contents": file_contents,
            # We temporarily store the dependency map in ast_metadata to seed the Knowledge Graph
            "ast_metadata": {"dependency_graph": dependency_map}, 
            "current_agent": "RepositoryAgent",
            "execution_status": "COMPLETED",
            "logs": [f"Repository Agent mapped {total_files} files and extracted initial dependency graphs."]
        }

# Expose a singleton instance for the workflow orchestrator
repository_agent_instance = RepositoryAgent()