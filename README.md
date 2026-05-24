# AI-Product-OPS

Набор AI-агентов для продуктового офиса.

## Агенты

### [Classificator](./Classificator)

Агент-классификатор инициатив **Продукт / Проект** (Initiative Classifier v10).

Через итеративный диалог анализирует инициативу по 8 критериям и выдаёт обоснованное заключение с процентной оценкой и рекомендациями по модели управления.

**Стек:** Python · Anthropic SDK · Streamlit

```bash
cd Classificator && pip install -r requirements.txt && streamlit run app.py
```