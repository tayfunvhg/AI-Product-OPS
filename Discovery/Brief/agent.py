import anthropic
from system_prompt import SYSTEM_PROMPT

WELCOME_MESSAGE = "Привет! Помогу написать продуктовый бриф. Опишите инициативу своими словами или загрузите любые материалы — презентацию, описание, черновик задачи. Я задам уточняющие вопросы и соберу полный бриф, готовый к передаче в команду."

MODEL = "claude-opus-4-7"


class BriefWriterAgent:
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
