import os

import streamlit as st
from dotenv import load_dotenv

from agent import VisionAssessorAgent

load_dotenv()

st.set_page_config(
    page_title="Vision Assessor",
    page_icon="📋",
    layout="centered",
)

st.title("Vision Assessor")
st.caption("Оценка продуктового видения по 6 критериям")

with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input(
        "Anthropic API Key",
        value=os.getenv("ANTHROPIC_API_KEY", ""),
        type="password",
        help="Получить ключ: console.anthropic.com",
    )
    st.divider()
    st.markdown(
        """
*Критерии оценки:*
1. Структурная целостность
2. Временной горизонт (3+ лет)
3. Клиентоцентричность
4. Ценность для бизнеса
5. Цели и метрики
6. Связь со стратегией

*Шкала:* Ok / Частично / Не проходит

*Оценка ИЗИ:*
- 5-6 Ok → Готово к использованию
- 4-5 Ok → Нужна доработка
- 0-3 Ok → Требует переработки
"""
    )

st.markdown("Вставьте продуктовое видение целиком — формулировку, стратегию, цели и контекст.")

vision_input = st.text_area(
    "Продуктовое видение",
    placeholder="Вставьте текст видения сюда...",
    height=300,
    label_visibility="collapsed",
)

evaluate_btn = st.button("Оценить", type="primary", use_container_width=True)

if evaluate_btn:
    if not api_key:
        st.error("Введите Anthropic API Key в боковой панели.")
        st.stop()
    if not vision_input.strip():
        st.warning("Вставьте текст видения для оценки.")
        st.stop()

    with st.spinner("Анализирую..."):
        try:
            agent = VisionAssessorAgent(api_key)
            result = agent.evaluate(vision_input)
            st.divider()
            st.markdown(result)
        except Exception as e:
            st.error(f"Ошибка: {e}")
