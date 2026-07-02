import logging
import sys

def setup_logger(name: str = "AI_OS") -> logging.Logger:
    """Configures a standardized, asynchronous-friendly logger."""
    logger_instance = logging.getLogger(name)
    
    # Prevent duplicate logs if instantiated multiple times
    if logger_instance.hasHandlers():
        return logger_instance

    logger_instance.setLevel(logging.DEBUG)

    # Create console handler with a higher log level
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Create a standardized OS-level formatting string
    # e.g., [2026-07-01 10:24:27] [INFO] [AI_OS] Repository Agent initialized...
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    console_handler.setFormatter(formatter)
    logger_instance.addHandler(console_handler)

    return logger_instance

# Global singleton imported by all agents
logger = setup_logger()