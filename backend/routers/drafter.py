"""FastAPI router for the Drafter agent."""

import sys
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

AGENT_DIRECTORY = Path(__file__).resolve().parents[2] / "agents" / "drafter"
sys.path.insert(0, str(AGENT_DIRECTORY))

from Drafter import AgentConfigurationError, DRAFTER  # noqa: E402

router = APIRouter(prefix="/api/agents/drafter", tags=["drafter"])


class DraftRequest(BaseModel):
    message: str
    session_id: str | None = None


@router.get("/health")
def health() -> dict[str, Any]:
    return DRAFTER.status()


@router.post("/draft")
def draft(request: DraftRequest) -> dict[str, str | None]:
    try:
        return DRAFTER.respond(request.session_id, request.message)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except AgentConfigurationError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail="Drafter could not complete that request.") from error
