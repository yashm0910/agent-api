from sqlalchemy import Column, Integer, Text, String, Boolean, JSON, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    review_text = Column(Text, nullable=False)

    signals = Column(JSON)   # entire signals object
    insights = Column(JSON)  # entire insights object

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())