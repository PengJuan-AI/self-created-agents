"""Serve the agents hub and the independent agent modules locally."""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
HUB_INDEX = Path(__file__).resolve().parent / "index.html"


class HubRequestHandler(SimpleHTTPRequestHandler):
    """Serve repository files while using the Hub as the root page."""

    def do_GET(self) -> None:  # noqa: N802
        if self.path in {"", "/", "/index.html"}:
            self.path = "/hub/index.html"
        super().do_GET()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local agents hub.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    handler = partial(HubRequestHandler, directory=str(REPOSITORY_ROOT))
    with ThreadingHTTPServer((args.host, args.port), handler) as server:
        print(f"Agent Hub is running at http://{args.host}:{args.port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nAgent Hub stopped.")


if __name__ == "__main__":
    main()
