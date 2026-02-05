import os
from dotenv import load_dotenv

load_dotenv()

import httpx
import json
import logging
from typing import Optional, Dict, Any, List
from app.models import ModelType, CompletionCriteria

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UNBOUND_API_URL = os.environ.get("UNBOUND_API_URL", "https://api.getunbound.ai/v1/chat/completions")
API_KEY = os.environ.get("UNBOUND_API_KEY")

class UnboundService:

    def __init__(self):
        self.api_key = os.environ.get("UNBOUND_API_KEY")
        if not self.api_key:
            logger.warning("UNBOUND_API_KEY not found in environment variables")

    
    async def call_llm(self, model: ModelType, prompt: str, system_prompt: str = "You are a helpful assistant.") -> Dict[str, Any]:
        """
        Calls the Unbound API.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model.value,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(UNBOUND_API_URL, headers=headers, json=payload, timeout=60.0)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"LLM Call failed: {e}")
            raise

    async def validate_output(self, output: str, criteria: CompletionCriteria) -> bool:
        """
        Validates the output based on criteria.
        """
        if criteria.type == "contains":
            if not criteria.value:
                return True
            logger.info(f"Validating 'contains': Value='{criteria.value}' in Output='{output[:50]}...'?")
            found = criteria.value.lower() in output.lower()
            logger.info(f"Result: {found}")
            return found
            
        elif criteria.type == "json_valid":
            try:
                json.loads(output)
                return True
            except:
                return False
                
        elif criteria.type == "llm_judge":
            # Use a cheaper model (or the same one) to judge
            judge_prompt = f"""
            Task: Evaluate if the following text meets the requirement.
            Requirement: {criteria.instruction}
            
            Text to evaluate:
            {output}
            
            Answer ONLY with 'YES' or 'NO'.
            """
            try:
                # Using K2P5 as judge mainly for speed/cost if available, or just reuse default
                response = await self.call_llm(ModelType.KIMI_K2P5, judge_prompt, system_prompt="You are an impartial judge.")
                answer = response['choices'][0]['message']['content'].strip().upper()
                return "YES" in answer
            except Exception as e:
                logger.error(f"Judge failed: {e}")
                return False # Fail safe
                
        return True # Default pass if no criteria
