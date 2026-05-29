import json
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

from datetime import datetime , timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR,"klm_baggage.txt")

loader = TextLoader(FILE_PATH)
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size = 1000 , chunk_overlap = 200)
split = splitter.split_documents(docs)
vector_store = Chroma.from_documents(documents=split , embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))
retriever = vector_store.as_retriever()
template = """You are a helpful AI Agent.Answer the user from only the documents he has attached. If u cant find the desired answer then just say " I couldnt find the desired answer" .Never make up facts or number
context: {context},
question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
llm = ChatGroq(model="llama-3.3-70b-versatile",temperature=0)
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
rag_chain = (
{"context": retriever | format_docs, "question": RunnablePassthrough()}
| prompt
| llm
| StrOutputParser()
)


def check_flight(start:str , end: str)-> str:
    """Checks whether there is a flight between the start and the end point .
    Args: 
        start: Departure Airport Code Eg JFK
        end:   Arrival Airport Code  Eg AMS
    
    
    """

    result = {
        "start" : start,
        "end": end,
        "flight_name" : "KLM_400",
        "flight" : "KLM",
        "datetime": str(datetime.now() + timedelta(hours=2)),

        
    }

    return json.dumps(result)


def book_flight(start:str , end: str , flight_name:str , flight:str)-> str:
    """Books the  flight for the user between the start and the end point .
    Args: 
        start: Departure Airport Code Eg JFK
        end:   Arrival Airport Code  Eg AMS
        flight_name: The  flight that will be going from the departure airport to arrival airport Eg KLM_400
        flight : The name of the flight Eg KLM

    
    
    """

    result = {
        "start" : start,
        "end": end,
        "flight_name" : flight_name,
        "flight" : flight

        
    }

    return json.dumps(result)

def book_complaint(name:str , mail: str , text:str) ->str:
    """Books the complain for the user who is not happy with the service of the airline he used
    Args:
        name: The name of the customer Eg: Rahul
        mail: The email-id of the customer Eg: rahul@gmail.com
        text: The text the customer writes to the airline Eg Dear klm , ur service was really poor my food was served cold and seats were torn and no wifi was there for people to work while on the place wont recommend it to anyone
    
    
    
    """
    result = {
        "name":name,
        "mail": mail,
        "text":text,
        "status":"success",
    }
    return json.dumps(result)



def rag_tool(query: str) -> str:

    """Search KLM baggage policy and guidelines to answer questions about baggage allowances, 
    restrictions, special items, and cabin baggage rules.
    Args:
        query: User question about KLM baggage e.g. "What is the cabin baggage limit for KLM?"
    """
    
    result_1 = rag_chain.invoke(query)
    result = {
        query:result_1
    }
    return json.dumps(result)

TOOLS = [check_flight, book_flight, book_complaint , rag_tool]





