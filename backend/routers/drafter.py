"""FastAPI router for the Drafter agent."""

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.adapters.drafter import AgentConfigurationError, DrafterAdapter

router = APIRouter(prefix="/api/agents/drafter", tags=["drafter"])
adapter = DrafterAdapter()


class DraftRequest(BaseModel):
    message: str
    session_id: str | None = None


@router.get("/health")
def health() -> dict[str, Any]:
    return adapter.health()


@router.post("/draft")
def draft(request: DraftRequest) -> dict[str, str | None]:
    try:
        return adapter.run({"message": request.message, "session_id": request.session_id})
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except AgentConfigurationError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail="Drafter could not complete that request.") from error
