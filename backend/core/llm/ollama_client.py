import httpx
import json
from typing import Dict, Any, Optional
from utils.logger import logger
from config import OLLAMA_BASE_URL, OLLAMA_MODEL

class OllamaClient:
    def __init__(self, base_url: str = OLLAMA_BASE_URL, default_model: str = OLLAMA_MODEL):
        self.base_url = base_url.rstrip('/')
        self.default_model = default_model
        self.timeout = httpx.Timeout(60.0, connect=10.0)

    async def generate_structured_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Queries Ollama with strict structural expectations. Forces JSON output constraints
        and handles syntax recoveries if the local model misbehaves.
        """
        target_model = model or self.default_model
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": target_model,
            "prompt": prompt,
            "format": "json",
            "stream": False,
            "options": {
                "temperature": 0.2,
                "top_p": 0.9
            }
        }
        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                result_json = response.json()
                raw_response_text = result_json.get("response", "{}")
                
                return json.loads(raw_response_text)
            except httpx.HTTPStatusError as exc:
                logger.error(f"Ollama server responded with error status: {exc.response.status_code}")
                return {"error": "HTTP failure", "details": str(exc)}
            except json.JSONDecodeError:
                logger.warning("Ollama output was not valid JSON. Attempting structural recovery block extraction.")
                return self._recover_malformed_json(raw_response_text)
            except Exception as e:
                logger.error(f"Unexpected connectivity failure with Ollama: {str(e)}")
                return {"error": "System connectivity fault", "details": str(e)}

    def _recover_malformed_json(self, raw_text: str) -> Dict[str, Any]:
        """Fallback heuristics to scrape embedded JSON markers if local LLM leaks prose."""
        try:
            start_idx = raw_text.find("{")
            end_idx = raw_text.rfind("}")
            if start_idx != -1 and end_idx != -1:
                return json.loads(raw_text[start_idx:end_idx + 1])
        except Exception:
            pass
        return {"error": "JSON parsing failure", "raw_payload": raw_text}

# Global Instance - This is what the Compiler Agent is looking for!
ollama_ai = OllamaClient()