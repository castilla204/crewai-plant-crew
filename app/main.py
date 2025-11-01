from fastapi import FastAPI

from app.config import settings
from app.crew_runner import run_crew
from app.models import RunRequest, RunResponse

app = FastAPI(title="CrewAI Plant Crew", version="0.1.0")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "mode": "crewai" if settings.use_crewai else "offline",
        "model": settings.openai_model if settings.use_crewai else None,
    }


@app.post("/run", response_model=RunResponse)
def run(req: RunRequest):
    result = run_crew(req.task)
    return RunResponse(task=req.task, **result)
