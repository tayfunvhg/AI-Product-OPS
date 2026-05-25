import os

import streamlit as st
from dotenv import load_dotenv

from agent import HypothesisGeneratorAgent, WELCOME_MESSAGE

load_dotenv()

st.set_page_config(
    page_title="Hypothesis Generator",
    page_icon="💡",
    layout="centered",
)

st.title("Hypothesis Generator")
st.caption("Генератор продуктовых гипотез на основе контекста")

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
*Что загружать:*
- Видение и стратегия продукта
- Брифы и описания инициатив
- Текущие метрики и данные
- Результаты исследований
- Бэклог и прошлые эксперименты

*Минимум 2 блока контекста для генерации.*

*Уверенность гипотез:*
- Высокая — есть метрики + данные
- Средняя — есть метрики, нет данных
- Низкая — метрики отсутствуют
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

if prompt := st.chat_input("Опишите инициативу или вставьте материалы..."):
    if not api_key:
        st.error("Введите Anthropic API Key в боковой панели.")
        st.stop()

    if st.session_state.agent is None:
        st.session_state.agent = HypothesisGeneratorAgent(api_key)

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Анализирую..."):
            try:
                response = st.session_state.agent.chat(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Ошибка: {e}")
