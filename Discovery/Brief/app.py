import os

import streamlit as st
from dotenv import load_dotenv

from agent import BriefWriterAgent, WELCOME_MESSAGE

load_dotenv()

st.set_page_config(
    page_title="Brief Writer",
    page_icon="📝",
    layout="centered",
)

st.title("Brief Writer")
st.caption("Составление продуктового брифа через диалог")

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
        st.session_state.messages = []
        st.session_state.agent = None
        st.rerun()
    st.divider()
    st.markdown(
        """
*Что войдёт в бриф:*
1. Что делаем (скоуп)
2. Зачем (полезное действие)
3. Для кого (пользователи)
4. Текущая ситуация
5. Критерии приёмки
6. Вне скоупа
7. Ограничения
8. RICE-приоритизация
9. Метрики успеха
10. Риски

*Бриф формируется при неопределённости ≤ 10%.*
"""
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = None

if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": WELCOME_MESSAGE})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Опишите инициативу или задайте вопрос..."):
    if not api_key:
        st.error("Введите Anthropic API Key в боковой панели.")
        st.stop()

    if st.session_state.agent is None:
        st.session_state.agent = BriefWriterAgent(api_key)

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Думаю..."):
            try:
                response = st.session_state.agent.chat(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Ошибка: {e}")
