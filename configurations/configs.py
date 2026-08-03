from pathlib import Path

from configurations.logger import get_logger

MODEL_NAME = "llama-3.3-70b-versatile"
PORT = 9000

logger = get_logger("config")

Base_dir = Path.cwd().resolve()


def get_relative_path(file_path:str) -> Path:
    
    """Convert relative path to absolute path within project directory.

    Ensures the path is within BASE_DIR for security. Resolves the path
    and validates it's relative to the base directory.

    Args:
        relative_path: Relative path string to convert

    Returns:
        Absolute Path object within BASE_DIR

    Raises:
        ValueError: If path is outside base directory
    """
    
    try:
        if not file_path:
            raise ValueError("File path is missing")
        
        path = (Base_dir / file_path).resolve()
        
        rel = path.relative_to(Base_dir)
        return rel
        
    except ValueError as e:
        logger.error(f"Path is outside Base_dir: {e}")
        raise
    
    except Exception as e:
        logger.error(f"Error in configs: {e}")
        raise