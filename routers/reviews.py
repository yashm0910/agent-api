from fastapi import APIRouter
from sqlalchemy import text
from database import SessionLocal

router = APIRouter()

@router.get("/reviews/sentiment/{sentiment}")
def get_reviews_for_Sentiment(sentiment:str):
    db=SessionLocal()
    results = db.execute(
        text("""
            SELECT * FROM reviews
            WHERE signals->>'sentiment' = :sentiment
        """),
        {"sentiment": sentiment}
    ).mappings().all()

    db.close()

    return results

@router.get("/reviews/category/{category}")
def get_by_category(category: str):
    db = SessionLocal()

    results = db.execute(
        text("""
            SELECT * FROM reviews
            WHERE signals->>'problem_category' = :category
        """),
        {"category": category}
    ).mappings().all()

    db.close()

    return results