from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
from typing import TypedDict,Literal,List,Optional
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from langchain_core.messages import SystemMessage,HumanMessage
import os

load_dotenv()

model= ChatGroq(
    model="openai/gpt-oss-20b", 
    api_key=os.getenv("api_key"),
)

class ReviewSignals(BaseModel):
    summary: str
    main_topic: str
    sentiment: Literal["positive","negative","neutral","mixed"]
    emotions_detected: List[str]
    positive_points: List[str]
    negative_points: List[str]
    confusion_level: Literal["none","mild","moderate","severe"]
    anger_level: Literal["low","medium","high"]
    feedback_clarity:Literal["clear","vague","contradictory"]
    problem_category:Literal["billing","support","onboarding","product_bug","feature_request","pricing"]

class ReviewInsights(BaseModel):
    satisfaction_level: Literal[
        "very_satisfied",
        "satisfied",
        "neutral",
        "dissatisfied",
        "very_dissatisfied"
    ]
    follow_up_recommendation:bool
    follow_up_reason:Optional[str]    
    improvement_suggestions: List[str]


structured_model_signals=model.with_structured_output(ReviewSignals)
structured_model_insights=model.with_structured_output(ReviewInsights)


class ReviewState(TypedDict):
    review_text: str
    signals: Optional[ReviewSignals]
    insights: Optional[ReviewInsights]



def review_analyis(state:ReviewState):
    review_text=state['review_text']
    prompt = f"""
    Analyze the following customer review and extract structured signals.

    - Provide short summary
    - Identify main topic
    - Classify sentiment
    - List emotions
    - Extract positive and negative points
    - Indicate confusion level in the review text
    - Anger level in the review text 
    - How clear customer is in giving review
    - What problem customer has targetted

    Only extract information supported by the text.

    Review:
    {review_text}
    """
    signals=structured_model_signals.invoke(prompt)
    return {
        "signals":signals
    }

def review_insights(state:ReviewState):
    signals=state['signals']
    review_text=state['review_text']
    prompt=f"""
    Analyze the following customer review and signals and extract following insights.
    
    - Satisfaction level as :
    [
        "very_satisfied",
        "satisfied",
        "neutral",
        "dissatisfied",
        "very_dissatisfied"
    ]
    - does customer neeeds to be followed up ? (True or False)
    - why customer to be followed back , for fixing problem or for making better customer relationship by advising more good services ?
    - what improvment suggestions you will suggest to the company
    
    
    Signals:
    signals= {state['signals']}
    
    Review text:
    review_text={state['review_text']}
    """
    
    insights=structured_model_insights.invoke(prompt)
    
    return {
        "insights":insights
    }

graph=StateGraph(ReviewState)

graph.add_node("analysis",review_analyis)
graph.add_node("insight",review_insights)

graph.add_edge(START,"analysis")
graph.add_edge("analysis","insight")
graph.add_edge("insight",END)

workflow=graph.compile()

# review="""
# Okay so I’ve been using your Pro subscription for around 3 months now. At first everything was smooth and honestly I liked the dashboard and analytics were actually accurate compared to other tools we tried.
# But last week things started getting weird. My invoice suddenly showed an extra charge and I couldn’t understand what it was for. There was no proper breakdown, just some “adjustment fee” label. I checked the docs and they don’t explain it clearly either. Maybe I missed something but it’s confusing.
# Also I upgraded because it said “24/7 priority support” but when I submitted a ticket on Sunday, I got a response almost 18 hours later. That doesn’t feel like priority. The support person was polite though, so I don’t blame them personally.
# I’m not super angry or anything, just annoyed because I recommended this tool to my team and now they’re questioning it. If billing and support clarity were improved, I’d be happy to continue using it. Right now I’m unsure whether to renew next quarter.
# """

# initial_state={
#     "review_text":review
# }

# result=workflow.invoke(initial_state)

# result['signals'].dict()

# result['insights'].dict()

def run_agent(review_text: str):
    initial_state = {"review_text": review_text}
    result = workflow.invoke(initial_state)
    return result