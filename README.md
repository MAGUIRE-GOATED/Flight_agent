# Flight Agent
A flight booking agent built with LangGraph and RAG. Demonstrates how LLMs use 
tool calling to handle user queries without relying on live web search.

## What it does
- Book flights between airports
- Check flight availability  
- File complaints
- Answer KLM baggage policy questions (RAG powered)

## IMPORTANT NOTE
This is a framework/demonstration project. It uses hardcoded flight data, not real airline APIs. The RAG tool retrieves from KLM's baggage policy pages — 
not a live search tool like Tavily.

## Tech Stack
- LangGraph — agent graph and tool routing
- Groq (llama-3.3-70b) — LLM
- ChromaDB — vector store
- HuggingFace embeddings — local embeddings
- LangChain — RAG pipeline

## How to run
1. Clone the repo
2. Create venv and install requirements
3. Add GROQ_API_KEY to .env
4. Run python main.py

## Architecture
See [ARCHITECTURE.md](ARCHITECTURE.md) for a breakdown of the codebase.


