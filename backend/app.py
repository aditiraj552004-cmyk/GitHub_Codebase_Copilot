from fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import (
    CORSMiddleware
)

from pydantic import BaseModel

from rag import answer_question

from ingest_github import (
    ingest_github_repo
)


app = FastAPI(
    title="GitHub Codebase Copilot",
    description=(
        "RAG-powered AI assistant "
        "for GitHub repositories"
    ),
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RepositoryRequest(BaseModel):

    repo_url: str


class QuestionRequest(BaseModel):

    repository_id: str

    question: str


@app.get("/")
def home():

    return {
        "message":
            "GitHub Codebase Copilot "
            "API is running"
    }


@app.post("/ingest")
def ingest_repository(
    request: RepositoryRequest
):

    try:

        return ingest_github_repo(
            request.repo_url
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/ask")
def ask_question(
    request: QuestionRequest
):

    try:

        answer, sources = (
            answer_question(
                request.question,
                request.repository_id
            )
        )

        return {
            "question":
                request.question,

            "answer":
                answer,

            "sources":
                sources
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )