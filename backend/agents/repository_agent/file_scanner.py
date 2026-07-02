import os
from typing import Dict, List, Tuple
from utils.logger import logger

class FileScanner:
    """Handles safe, OS-agnostic file traversal and encoding resolution."""
    
    def __init__(self):
        self.ignore_dirs = {
            '.git', 'node_modules', '__pycache__', 'venv', 'env', 
            '.venv', 'dist', 'build', '.idea', '.vscode', 'coverage'
        }
        self.ignore_exts = {
            '.pyc', '.png', '.jpg', '.jpeg', '.gif', '.pdf', '.exe', 
            '.dll', '.so', '.zip', '.tar', '.gz', '.mp4', '.sqlite3'
        }
        self.encodings = ['utf-8', 'latin-1', 'cp1252']

    def safe_read(self, filepath: str) -> str:
        """Attempts to read a file using multiple fallback encodings."""
        for encoding in self.encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.error(f"OS read error on {filepath}: {str(e)}")
                return ""
        logger.warning(f"Decoding failed for {filepath}. Skipping.")
        return ""

    def scan_directory(self, root_path: str) -> Dict[str, str]:
        """Walks the directory and returns a dictionary of relative paths to file contents."""
        file_contents = {}
        if not os.path.exists(root_path):
            return file_contents

        for dirpath, dirnames, filenames in os.walk(root_path):
            dirnames[:] = [d for d in dirnames if d not in self.ignore_dirs]

            for filename in filenames:
                ext = os.path.splitext(filename)[1].lower()
                if ext in self.ignore_exts:
                    continue

                full_path = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(full_path, root_path).replace("\\", "/")
                
                content = self.safe_read(full_path)
                if content:
                    file_contents[relative_path] = content

        return file_contents