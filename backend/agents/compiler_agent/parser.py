import ast
from typing import Tuple, Optional
from utils.logger import logger

class Parser:
    """Validates the token stream against the language grammar."""
    
    @staticmethod
    def validate_syntax(code_content: str, filename: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Returns True if syntax is valid, or False with the error details."""
        try:
            # The parser strictly checks for structural integrity
            ast.parse(code_content, filename=filename)
            return True, None
        except SyntaxError as e:
            error_details = {
                "error_message": e.msg,
                "line_number": e.lineno,
                "offset": e.offset,
                "text": e.text
            }
            return False, error_details