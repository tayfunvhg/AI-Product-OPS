import anthropic
from system_prompt import SYSTEM_PROMPT

MODEL = "claude-opus-4-7"


class VisionAssessorAgent:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def evaluate(self, vision_text: str) -> str:
        response = self.client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": vision_text}],
        )
        return response.content[0].text
