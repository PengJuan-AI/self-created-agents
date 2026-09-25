"""Drafter's HTTP backend and local development server.

Run this file directly, then open http://127.0.0.1:8000 in a browser.
"""

from __future__ import annotations

import argparse
import json
import os
import threading
from dataclasses import dataclass, field
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from uuid import uuid4

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # The server can still render the UI and report its missing AI dependency.
    pass


PROJECT_DIRECTORY = Path(__file__).resolve().parent
STATIC_DIRECTORY = PROJECT_DIRECTORY / "static"
DOCUMENT_DIRECTORY = PROJECT_DIRECTORY / "documents"
MAX_REQUEST_BYTES = 64 * 1024
MAX_MESSAGE_LENGTH = 12_000
MAX_HISTORY_MESSAGES = 24


class AgentConfigurationError(RuntimeError):
    """Raised when the optional LLM integration is not ready to use."""


@dataclass
class DraftSession:
    """A browser session's conversation and working document."""

    document: str = ""
    messages: list[Any] = field(default_factory=list)
    last_saved_file: str | None = None
    lock: threading.RLock = field(default_factory=threading.RLock, repr=False)


class DrafterService:
    """Coordinates isolated document sessions with the DeepSeek drafting model."""

    def __init__(self) -> None:
        self._sessions: dict[str, DraftSession] = {}
        self._sessions_lock = threading.Lock()
        self._model: Any | None = None
        self._model_lock = threading.Lock()

    def status(self) -> dict[str, Any]:
        if not os.getenv("DEEPSEEK_API_KEY"):
            return {
                "ready": False,
                "message": "Set DEEPSEEK_API_KEY to enable Drafter responses.",
            }

        try:
            import langchain_deepseek  # noqa: F401
        except ImportError:
            return {
                "ready": False,
                "message": "Install the dependencies in requirements.txt to enable Drafter.",
            }

        return {"ready": True, "message": "Drafter is ready."}

    def respond(self, session_id: str | None, user_input: str) -> dict[str, str | None]:
        message = user_input.strip()
        if not message:
            raise ValueError("Enter a drafting request before sending it.")
        if len(message) > MAX_MESSAGE_LENGTH:
            raise ValueError(f"Keep requests under {MAX_MESSAGE_LENGTH:,} characters.")

        resolved_session_id, session = self._get_session(session_id)
        with session.lock:
            response_text = self._run_agent(session, resolved_session_id, message)
            return {
                "session_id": resolved_session_id,
                "response": response_text,
                "document": session.document,
                "saved_file": session.last_saved_file,
            }

    def _get_session(self, session_id: str | None) -> tuple[str, DraftSession]:
        normalized_id = session_id if isinstance(session_id, str) else ""
        with self._sessions_lock:
            if normalized_id and normalized_id in self._sessions:
                return normalized_id, self._sessions[normalized_id]

            new_id = str(uuid4())
            session = DraftSession()
            self._sessions[new_id] = session
            return new_id, session

    def _get_model(self) -> Any:
        if self._model is not None:
            return self._model

        with self._model_lock:
            if self._model is not None:
                return self._model
            if not os.getenv("DEEPSEEK_API_KEY"):
                raise AgentConfigurationError("Set DEEPSEEK_API_KEY to enable Drafter responses.")

            try:
                from langchain_deepseek import ChatDeepSeek
            except ImportError as error:
                raise AgentConfigurationError(
                    "Install the dependencies in requirements.txt to enable Drafter."
                ) from error

            self._model = ChatDeepSeek(
                model=os.getenv("DEEPSEEK_MODEL", "deepseek-v4-pro"),
                max_tokens=1_000,
            )
            return self._model

    def _create_tools(self, session: DraftSession, session_id: str) -> list[Any]:
        from langchain_core.tools import tool

        @tool("update_document")
        def update_document(content: str) -> str:
            """Replace the working document with the complete updated document content."""
            session.document = content
            return "Document updated."

        @tool("save_document")
        def save_document(filename: str) -> str:
            """Save the current document as a text file when the user explicitly asks to save it."""
            safe_name = Path(filename.strip()).name
            if safe_name in {"", ".", ".."}:
                return "A valid filename is required to save the document."
            if not safe_name.endswith(".txt"):
                safe_name = f"{safe_name}.txt"

            DOCUMENT_DIRECTORY.mkdir(parents=True, exist_ok=True)
            saved_name = f"{session_id[:8]}-{safe_name}"
            (DOCUMENT_DIRECTORY / saved_name).write_text(session.document, encoding="utf-8")
            session.last_saved_file = saved_name
            return f"Document saved as {saved_name}."

        return [update_document, save_document]

    def _run_agent(self, session: DraftSession, session_id: str, user_input: str) -> str:
        # Validate the configured model before importing the optional message and tool SDKs.
        model = self._get_model()
        from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
        tools = self._create_tools(session, session_id)
        tools_by_name = {tool.name: tool for tool in tools}
        model = model.bind_tools(tools)
        system_message = SystemMessage(
            content=(
                "You are Drafter, a concise and helpful writing assistant. "
                "Draft, revise, or polish documents based on the user's request. "
                "When changing the document, call update_document with the full revised text. "
                "Only call save_document when the user explicitly asks to save. "
                "After a document update, give a concise response and include the current document.\n\n"
                f"Current document:\n{session.document or '(empty)'}"
            )
        )
        turn_messages: list[Any] = [HumanMessage(content=user_input)]
        conversation = [system_message, *session.messages[-MAX_HISTORY_MESSAGES:], *turn_messages]

        for _ in range(4):
            response = model.invoke(conversation)
            turn_messages.append(response)
            conversation.append(response)
            tool_calls = getattr(response, "tool_calls", []) or []
            if not tool_calls:
                session.messages.extend(turn_messages)
                content = str(response.content).strip()
                return content or session.document or "Your document is ready for the next instruction."

            for call in tool_calls:
                tool_name = call.get("name", "")
                tool = tools_by_name.get(tool_name)
                if tool is None:
                    result = f"The requested tool '{tool_name}' is not available."
                else:
                    result = tool.invoke(call.get("args", {}))
                tool_message = ToolMessage(
                    content=str(result),
                    tool_call_id=call.get("id", tool_name),
                )
                turn_messages.append(tool_message)
                conversation.append(tool_message)

        session.messages.extend(turn_messages)
        return session.document or "I could not complete that drafting step. Please try again."


DRAFTER = DrafterService()


class DrafterRequestHandler(SimpleHTTPRequestHandler):
    """Serve the static interface and the JSON drafting endpoint."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(STATIC_DIRECTORY), **kwargs)

    def do_GET(self) -> None:  # noqa: N802
        if urlparse(self.path).path == "/api/health":
            self._send_json(HTTPStatus.OK, DRAFTER.status())
            return
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path != "/api/draft":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found."})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            content_length = 0
        if content_length <= 0 or content_length > MAX_REQUEST_BYTES:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Request body is invalid or too large."})
            return

        try:
            payload = json.loads(self.rfile.read(content_length))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Request body must be valid JSON."})
            return

        if not isinstance(payload, dict):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Request body must be a JSON object."})
            return

        try:
            result = DRAFTER.respond(payload.get("session_id"), payload.get("message", ""))
        except ValueError as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
        except AgentConfigurationError as error:
            self._send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": str(error)})
        except Exception:
            self._send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": "Drafter could not complete that request. Please try again."},
            )
        else:
            self._send_json(HTTPStatus.OK, result)

    def _send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        # Keep terminal output focused on server startup and application errors.
        return


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Drafter web interface.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    with ThreadingHTTPServer((args.host, args.port), DrafterRequestHandler) as server:
        print(f"Drafter is running at http://{args.host}:{args.port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nDrafter stopped.")


if __name__ == "__main__":
    main()
