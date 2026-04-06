# Review Intelligence Agent

## Overview

This project is an AI-powered backend system that analyzes product reviews and generates structured insights using LLM-based workflows. It automates the process of extracting meaningful information from large volumes of user reviews.

The system processes raw review data, classifies sentiment (positive, neutral, negative), and produces structured outputs that can be stored, queried, and used for further analysis.

---

## Key Features

* AI-based sentiment analysis using LLMs
* Structured output generation using Pydantic
* FastAPI-based REST APIs
* PostgreSQL integration for persistent storage
* Agent-style workflow for review processing
* Modular and scalable backend design

---

## System Flow

Input Reviews → LLM Processing (Sentiment + Insights) → Structured Output → Database Storage → API Retrieval / Filtering

---

## Tech Stack

* Backend: FastAPI
* Database: PostgreSQL
* AI/LLM: Groq / OpenAI via LangChain
* Workflow: LangGraph
* Data Handling: Pydantic, Pandas
* Deployment: Docker

---

## API Endpoints

### POST /ingest

Stores incoming review data in the database.

### POST /analyze

Processes reviews using LLM workflows and generates structured insights.

### GET /reviews?sentiment=positive

Retrieves reviews filtered by sentiment or other parameters.

---

## Example Output

```json
{
  "review": "Great product, works really well!",
  "sentiment": "positive",
  "confidence": 0.92,
  "insight": "Users appreciate product reliability and performance"
}
```

---

## Architecture Highlights

* Modular pipeline separating ingestion, processing, and retrieval
* LLM integrated with structured outputs for consistency
* Backend designed for extension into agent-based workflows
* Database-backed system for persistence and querying

---

## Future Improvements

* Tool-based agent workflows (dynamic decision making)
* MCP integration for external tool orchestration
* Dashboard generation for insights visualization
* Caching (Redis) to optimize repeated analysis
* Background processing for scalability

---

## Running the Project

```bash
pip install -r requirements.txt
```

```bash
uvicorn main:app --reload
```

---

## Goal

The goal of this project is to build production-style AI backend systems that combine LLM reasoning, structured data processing, and scalable API design to solve real-world problems efficiently.
