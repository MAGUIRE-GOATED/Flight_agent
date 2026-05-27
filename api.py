from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from pydantic import BaseModel

from langchain_core.messages import HumanMessage




from Flight_agent.graph import graph
app = FastAPI()

# Define what the request body looks like
class ChatRequest(BaseModel):
    message: str

# Health check
@app.get("/")
def root():
    return {"message": "Flight Agent API is running"}

# Main chat endpoint
@app.post("/chat")
async def chat(request: ChatRequest):
    result = await graph.ainvoke({
        "messages": [HumanMessage(content=request.message)]
    })
    response = result["messages"][-1].content
    return {"response": response}