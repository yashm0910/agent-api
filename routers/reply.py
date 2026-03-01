from fastapi import APIRouter,HTTPException
from database import SessionLocal
from models import Review
from agent import model

router = APIRouter()

@router.get("/review/reply/{review_id}")
def get_reply(review_id:int):
    db = SessionLocal()
    review = db.query(Review).filter(Review.id == review_id).first()
    
    if not review:
        raise HTTPException(status_code=404,detail="review not found")
    
    prompt=f"""
    
    review_test: {review.review_text}
    review_signals: {review.signals}
    review_insights: {review.insights}
    
    generate a professional and concise company response in 50-60 words.
    
    If negative → apologize and assure resolution.
    If positive → thank and suggest additional services.
    If mixed → balance appreciation and apology.
    if neutral → Thank + request feedback for better clarity
    
    """
    reply = model.invoke(prompt).content
    
    return {
        "review_text":review.review_text,
        "company reply": reply
    }