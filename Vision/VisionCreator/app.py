import os

import streamlit as st
from dotenv import load_dotenv

from agent import VisionCreatorAgent, WELCOME_MESSAGE

load_dotenv()

st.set_page_config(
    page_title="Vision Creator",
    page_icon="🔭",
    layout="centered",
)

st.title("Vision Creator")
st.caption("Формирование продуктового видения")

with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input(
        "Anthropic API Key",
        value=os.getenv("ANTHROPIC_API_KEY", ""),
        type="password",
        help="Получить ключ: console.anthropic.com",
    )
    st.divider()
    if st.button("Начать заново", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": WELCOME_MESSAGE}
        ]
        st.session_state.agent = VisionCreatorAgent(api_key) if api_key else None
        st.rerun()
    st.divider()
    st.markdown(
        """
**Как работает агент:**
- Собирает информацию через диалог
- Отслеживает неопределённость и задаёт уточняющие вопросы
- Генерирует структурированное видение в 3 блоках

**Результат:**
- Блок 1: формулировка видения + ценность для пользователей
- Блок 2: стратегия по годам с ориентирами
- Блок 3: ключевые бизнес-цели с цифрами
"""
    )

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": WELCOME_MESSAGE}
    ]

if "agent" not in st.session_state:
    st.session_state.agent = VisionCreatorAgent(api_key) if api_key else None

if api_key and (
    st.session_state.agent is None
    or st.session_state.agent.client.api_key != api_key
):
    st.session_state.agent = VisionCreatorAgent(api_key)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Расскажите о продукте или пришлите материалы..."):
    if not api_key:
        st.error("Введите Anthropic API Key в боковой панели.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Думаю..."):
            try:
                response = st.session_state.agent.chat(prompt)
                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
            except Exception as e:
                st.error(f"Ошибка: {e}")
