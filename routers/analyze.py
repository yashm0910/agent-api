from fastapi import APIRouter
from pydantic import BaseModel
from database import SessionLocal
from models import Review
from agent import run_agent

router = APIRouter()

class ReviewRequest(BaseModel):
    review_text: str

@router.post("/analyze")
def analyze_review(request: ReviewRequest):
    result = run_agent(request.review_text)

    db = SessionLocal()
    db_review = Review(
        review_text=request.review_text,
        signals=result["signals"].model_dump(),
        insights=result["insights"].model_dump()
    )
    db.add(db_review)
    db.commit()
    db.close()

    return result