"""StudyStack API.

Run (from backend/):  uvicorn app.main:app --reload
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import ask, health, ingest

app = FastAPI(title="StudyStack", version="0.2.0")

app.add_middleware(  # lets a future Next.js frontend on another port call us
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(ask.router)
app.include_router(ingest.router)


@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception) -> JSONResponse:
    # Never leak stack traces to clients; log server-side instead.
    return JSONResponse(status_code=500, content={"detail": "Internal error"})
