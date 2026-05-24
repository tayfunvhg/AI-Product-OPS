import os

import streamlit as st
from dotenv import load_dotenv

from agent import ClassifierAgent, WELCOME_MESSAGE

load_dotenv()

st.set_page_config(
    page_title="Initiative Classifier",
    page_icon="🔍",
    layout="centered",
)

st.title("Initiative Classifier v10")
st.caption("Классификатор инициатив: Продукт / Проект")

# Sidebar
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
        st.session_state.agent = ClassifierAgent(api_key) if api_key else None
        st.rerun()
    st.divider()
    st.markdown(
        """
**Как работает агент:**
- Анализирует материалы инициативы
- Задаёт уточняющие вопросы
- Выдаёт обоснованное заключение: Продукт или Проект

**Шаги:**
1. Пришлите описание/презентацию
2. Отвечайте на вопросы агента
3. Получите классификацию с процентом
"""
    )

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": WELCOME_MESSAGE}
    ]

if "agent" not in st.session_state:
    st.session_state.agent = ClassifierAgent(api_key) if api_key else None

# Re-create agent if API key changes
if api_key and (
    st.session_state.agent is None
    or st.session_state.agent.client.api_key != api_key
):
    st.session_state.agent = ClassifierAgent(api_key)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Опишите вашу инициативу или задайте вопрос..."):
    if not api_key:
        st.error("Введите Anthropic API Key в боковой панели.")
        st.stop()

    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Анализирую..."):
            try:
                response = st.session_state.agent.chat(prompt)
                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
            except Exception as e:
                error_msg = f"Ошибка: {e}"
                st.error(error_msg)
