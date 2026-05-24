import anthropic
from system_prompt import SYSTEM_PROMPT

WELCOME_MESSAGE = """Привет! Помогу собрать продуктовое видение — компактное, с фокусом на то, **куда** идём, **для кого** и **какую ценность** создаём. Три способа начать:

**1. С нуля** — расскажи про продукт, задам уточняющие вопросы.
**2. С материалами** — пришли описание, презентации, метрики, исследования — проанализирую и спрошу по пробелам.
**3. Доработка** — пришли текущее видение, оценю и предложу улучшения.

Можно комбинировать."""

MODEL = "claude-opus-4-7"


class VisionCreatorAgent:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.history: list[dict] = []

    def chat(self, user_message: str) -> str:
        self.history.append({"role": "user", "content": user_message})

        response = self.client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=self.history,
        )

        assistant_message = response.content[0].text
        self.history.append({"role": "assistant", "content": assistant_message})
        return assistant_message

    def reset(self):
        self.history = []
