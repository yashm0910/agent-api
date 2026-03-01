from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from database import SessionLocal
from models import Review
from agent import run_agent,model
from models import Base
from database import engine
from sqlalchemy import text
from routers import analyze,reply,reviews

Base.metadata.create_all(bind=engine)

app = FastAPI()

class ReviewRequest(BaseModel):
    review_text: str
    
app.include_router(analyze.router)
app.include_router(reviews.router)
app.include_router(reply.router)


# @app.post("/analyze")
# def analyze_review(request:ReviewRequest):
    
#     result=run_agent(request.review_text)
#     db=SessionLocal()
    
#     db_review= Review(
#         review_text=request.review_text,
#         signals=result["signals"].model_dump(),
#         insights=result["insights"].model_dump()
#     )

#     db.add(db_review)
#     db.commit()
#     db.close()
    
#     return {
#         "signals": result["signals"],
#         "insights": result["insights"]
#     }
    
# @app.get("/reviews/sentiment/{sentiment}")
# def get_reviews_for_Sentiment(sentiment:str):
#     db=SessionLocal()
#     results = db.execute(
#         text("""
#             SELECT * FROM reviews
#             WHERE signals->>'sentiment' = :sentiment
#         """),
#         {"sentiment": sentiment}
#     ).mappings().all()

#     db.close()

#     return results

# @app.get("/reviews/category/{category}")
# def get_by_category(category: str):
#     db = SessionLocal()

#     results = db.execute(
#         text("""
#             SELECT * FROM reviews
#             WHERE signals->>'problem_category' = :category
#         """),
#         {"category": category}
#     ).mappings().all()

#     db.close()

#     return results

# @app.get("/review/reply/{review_id}")
# def get_reply(review_id:int):
#     db = SessionLocal()
#     review = db.query(Review).filter(Review.id == review_id).first()
    
#     if not review:
#         raise HTTPException(status_code=404,detail="review not found")
    
#     prompt=f"""
    
#     review_test: {review.review_text}
#     review_signals: {review.signals}
#     review_insights: {review.insights}
    
#     generate a professional and concise company response in 50-60 words.
    
#     If negative → apologize and assure resolution.
#     If positive → thank and suggest additional services.
#     If mixed → balance appreciation and apology.
#     if neutral → Thank + request feedback for better clarity
    
#     """
#     reply = model.invoke(prompt).content
    
#     return {
#         "review_text":review.review_text,
#         "company reply": reply
#     }

