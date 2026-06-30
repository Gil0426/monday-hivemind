#!/usr/bin/env python3
"""
mcp_http.py — remote (HTTP) launcher for the monday-hivemind MCP server.

Wraps the same server defined in mcp_server.py (all three tools) but serves it
over Streamable HTTP so it can be reached from Cowork and regular Claude chat
through a public tunnel (e.g. cloudflared).

Security: the server is mounted at a secret path derived from HIVEMIND_TOKEN in
.env. claude.ai custom connectors send the full URL path on every request, so a
caller who doesn't know the path gets a 404. Listens on localhost only — the
tunnel is the sole entry point.

Run:  .venv\\Scripts\\python.exe mcp_http.py
The connector URL is:  https://<your-tunnel-host>/mcp-<HIVEMIND_TOKEN>
"""

from __future__ import annotations
import os
import sys

import uvicorn

# Importing mcp_server runs its .env bootstrap and builds the FastMCP instance
# with all tools registered. Its __main__ guard means no stdio server starts.
from mcp_server import mcp
from mcp.server.transport_security import TransportSecuritySettings

_TOKEN = os.environ.get("HIVEMIND_TOKEN")
if not _TOKEN:
    sys.exit("ERROR: HIVEMIND_TOKEN is not set in .env — cannot start secured server.")

# Secret mount path acts as the shared secret (no custom-header support in the
# claude.ai connector UI, so the secret lives in the URL path instead).
mcp.settings.streamable_http_path = f"/mcp-{_TOKEN}"

# Disable the SDK's DNS-rebinding Host-header check. It only allows localhost by
# default, which 421s every request coming through the tunnel (the Host header is
# the public tunnel domain). That protection guards against malicious local web
# pages POSTing to a localhost MCP server; here our auth is the secret path, and
# the server binds to 127.0.0.1 reachable only via the tunnel, so disabling the
# host check is safe.
mcp.settings.transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=False
)

app = mcp.streamable_http_app()

if __name__ == "__main__":
    # Cloud hosts (Railway, Render, Fly, etc.) inject the port to bind via $PORT
    # and require binding all interfaces. Locally, serve_remote.py sets
    # HIVEMIND_HTTP_HOST=127.0.0.1 so the server stays localhost-only and the
    # cloudflared tunnel is the sole entry point.
    host = os.environ.get("HIVEMIND_HTTP_HOST", "0.0.0.0")
    port = int(os.environ.get("PORT") or os.environ.get("HIVEMIND_HTTP_PORT") or "8765")
    uvicorn.run(app, host=host, port=port)
