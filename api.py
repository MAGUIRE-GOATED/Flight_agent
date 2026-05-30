from dotenv import load_dotenv
load_dotenv()
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from graph import graph
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://luxury-youtiao-5bef59.netlify.app"],   # lock this down to your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define what the request body looks like
class ChatRequest(BaseModel):
    message: str
    session_id : str

# Health check
@app.get("/")
def root():
    return {"message": "Flight Agent API is running"}

# Main chat endpoint
@app.post("/chat")
async def chat(request: ChatRequest):
    config = {"configurable": {"thread_id": request.session_id}}
    result = await graph.ainvoke({
        "messages": [HumanMessage(content=request.message)]
    },
    config=config)
    response = result["messages"][-1].content
    return {"response": response}