import random
from app.database import SessionLocal
from app.models import Response

FEEDBACKS = [
    "Отличный продукт, всё устраивает",
    "Слишком дорого для моих задач",
    "Не хватает интеграций",
    "Быстрый и удобный",
    "Медленная поддержка",
    "Постоянные баги",
    "Пользуюсь каждый день",
    "Сложный интерфейс",
    "Хочу тёмную тему",
    "Не могу найти нужную функцию",
]

def seed(n=500):
    db = SessionLocal()
    try:
        for i in range(n):
            score = random.choices(
                range(0, 11),
                weights=[3,2,2,3,4,6,8,12,18,20,22]
            )[0]
            db.add(Response(
                user_id=f"u{i}",
                segment=random.choice(["free", "pro", "enterprise"]),
                survey_type="nps",
                score=score,
                feedback=random.choice(FEEDBACKS),
            ))
        db.commit()
        print(f"Seeded {n} responses")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
