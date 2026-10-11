# nps-csat-analyzer
 анализ NPS и CSAT опросов с NLP-кластеризацией отзывов. Расчёт метрик, разрез по сегментам, sentiment, темы жалоб. Дашборд для Customer Success.  Стек: FastAPI, PostgreSQL, sentence-transformers, scikit-learn, Streamlit, Docker, GitHub Actions

# nps-csat-analyzer

Анализ NPS и CSAT опросов с NLP-кластеризацией отзывов.

## Возможности
- Расчёт NPS (promoters / passives / detractors)
- CSAT по 5-балльной шкале
- Разрез по сегментам
- Кластеризация отзывов по темам
- Фильтр «только детракторы»
- Streamlit-дашборд

## Быстрый старт
cp .env.example .env
docker-compose up --build

API: http://localhost:8000/docs
Dashboard: http://localhost:8501

## Тесты
pytest tests/ -v

## Лицензия
MIT
