import tokenize
import io
from typing import List, Dict, Any
from utils.logger import logger

class Lexer:
    """Performs lexical analysis, breaking raw strings into token streams."""
    
    @staticmethod
    def tokenize_code(code_content: str) -> List[Dict[str, Any]]:
        tokens = []
        try:
            # Simulate a token stream using Python's built-in tokenize
            stream = io.BytesIO(code_content.encode('utf-8'))
            for tok in tokenize.tokenize(stream.readline):
                if tok.type != tokenize.ENCODING:
                    tokens.append({
                        "type": tokenize.tok_name[tok.type],
                        "string": tok.string,
                        "start": tok.start,
                        "end": tok.end
                    })
            return tokens
        except tokenize.TokenError as e:
            logger.warning(f"Lexical tokenization error: {e}")
            return []