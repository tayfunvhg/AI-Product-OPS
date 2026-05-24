import anthropic
from system_prompt import SYSTEM_PROMPT

WELCOME_MESSAGE = """Привет! Помогу определить, является ли ваша инициатива продуктом или проектом. Это важно для выбора модели управления — и тот, и другой тип одинаково ценны, вопрос лишь в том, какая модель будет эффективнее для достижения ваших бизнес-целей.

Для классификации мне нужны материалы — презентация, описание, шаблон или другие документы. Два способа начать:

1. Пришлите материалы — проанализирую и спрошу по пробелам.
2. Уже есть заполненный шаблон — пришлите, оценю и задам вопросы.

Если материалов пока нет, могу провести предварительную консультацию, но итоговая классификация потребует документов."""

MODEL = "claude-opus-4-7"


class ClassifierAgent:
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
