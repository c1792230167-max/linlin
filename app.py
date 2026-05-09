from fastapi import FastAPI
from pydantic import BaseModel

from retrieval_agent import RetrievalAgent

app = FastAPI(
    title="RAG Retrieval Agent",
    version="1.0.0"
)

agent = RetrievalAgent()


class AskRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {
        "message": "RAG Retrieval Agent Running"
    }


@app.post("/ask")
def ask(req: AskRequest):
    result = agent.answer(req.query)

    return {
        "query": result["query"],
        "answer": result["answer"],
        "sources": result["retrieved_docs"],
    }
