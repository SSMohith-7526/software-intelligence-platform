from typing import Dict, Any
from utils.logger import logger

class SharedContextManager:
    """
    Provides an out-of-band memory store for data that is too large 
    to pass constantly through the LangGraph state bus (e.g., raw binary mappings, 
    massive external library typings).
    """
    _instance = None
    _memory_store: Dict[str, Any] = {}

    def __new__(cls):
        # Singleton pattern ensures all agents talk to the same memory bank
        if cls._instance is None:
            cls._instance = super(SharedContextManager, cls).__new__(cls)
        return cls._instance

    def set_val(self, key: str, value: Any) -> None:
        self._memory_store[key] = value
        logger.debug(f"ContextManager: Stored key '{key}'.")

    def get_val(self, key: str, default: Any = None) -> Any:
        return self._memory_store.get(key, default)

    def clear_context(self) -> None:
        """Wipes volatile memory between pipeline runs."""
        self._memory_store.clear()
        logger.debug("ContextManager: Volatile memory cleared.")

# Global instance
global_context = SharedContextManager()