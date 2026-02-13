from anthropic import Anthropic
from app.core.config import settings
from typing import Optional

class ClaudeService:
    def __init__(self):
        self.client = None
        if settings.ANTHROPIC_API_KEY:
            self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            
    def generate_content(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate content using Claude.
        Note: Anthropic client is synchronous by default, but we can wrap it or use AsyncAnthropic if needed.
        For now using sync as per standard usage or switch to AsyncAnthropic.
        """
        if not self.client:
            raise ValueError("ANTHROPIC_API_KEY is not set in .env")
            
        messages = [{"role": "user", "content": prompt}]
        
        kwargs = {
            "model": settings.CLAUDE_MODEL,
            "max_tokens": 4096,
            "messages": messages
        }
        
        if system_prompt:
            kwargs["system"] = system_prompt
            
        response = self.client.messages.create(**kwargs)
        
        # Helper to extract text from response content
        if response.content and hasattr(response.content[0], 'text'):
            return response.content[0].text
        return ""

# Initialize global instance
claude_service = ClaudeService()
