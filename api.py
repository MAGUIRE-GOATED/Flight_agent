#Giving the agent a new home from terminal to a web server so that instead of putting ur prompts and running them in terminal a user can basically 
#run them from anywhere on the web. The agents u see on the web are basically ai architecture wrapped up in http endpoints and presented beautifully in a frontend ui .

from dotenv import load_dotenv
load_dotenv()
__import__('pysqlite3')   #chromodb uses sqlite but render linux servers operate on an older version of sqlite which wont work so pysqlite-3 is used so that chromadb can use that instead of the old sqlite
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')  #tricking chromadb to use pysqlite3 instead of sqlite3 by renaming it
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from graph import graph
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,  #javascript on one domain cannot talk to the server of another domain (same origin poilicy)
                     #without course middleware our api on render cannot talk to the frontend on netlify
    allow_origins=["https://luxury-youtiao-5bef59.netlify.app"],   # lock this down to the frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define what the request body looks like
class ChatRequest(BaseModel):
    message: str
    session_id : str

@app.get("/health")
def health():
    return {"status": "ok"}

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