#!/usr/bin/env python3
"""
serve_remote.py — one command to expose the hivemind to Cowork / Claude chat.

Cowork and regular Claude chat run in the cloud, so they can't reach a local
stdio MCP server. They need a *remote* MCP server with a public HTTPS URL. This
script starts the HTTP MCP server (mcp_http.py) and a cloudflared quick tunnel,
then prints the full connector URL (public tunnel host + your secret path) to
paste into Claude's "Add custom connector" dialog.

Run it yourself:   .venv\\Scripts\\python.exe serve_remote.py
or double-click:   serve_remote.bat

Leave the window open while you use the hivemind remotely. Ctrl+C stops both.

NOTES
- A free cloudflared tunnel gets a NEW hostname each run, so the connector URL
  changes every time — re-paste it into the connector. A stable URL needs a
  named Cloudflare tunnel and a domain you own.
- The server's only access control is the secret path in the URL (claude.ai's
  custom-connector dialog has no custom-header field). Keep the URL private.
"""

from __future__ import annotations
import os
import pathlib
import re
import secrets
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).parent.resolve()
ENV = HERE / ".env"


def _get_or_create_token() -> str:
    """Return HIVEMIND_TOKEN from .env, generating and persisting one if absent."""
    if not ENV.exists():
        sys.exit("No .env found. Copy .env.example to .env and add ANTHROPIC_API_KEY first.")
    for line in ENV.read_text(encoding="utf-8").splitlines():
        if line.startswith("HIVEMIND_TOKEN="):
            val = line.split("=", 1)[1].strip()
            if val:
                return val
    token = secrets.token_urlsafe(24)
    with ENV.open("a", encoding="utf-8") as f:
        f.write(f"\nHIVEMIND_TOKEN={token}\n")
    print("Generated a new HIVEMIND_TOKEN and saved it to .env (keep it private).")
    return token


def _find_cloudflared() -> pathlib.Path:
    candidates = [
        pathlib.Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "cloudflared" / "cloudflared.exe",
        pathlib.Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "cloudflared" / "cloudflared.exe",
        pathlib.Path("/usr/local/bin/cloudflared"),
        pathlib.Path("/usr/bin/cloudflared"),
    ]
    found = next((p for p in candidates if p.exists()), None)
    if found is None:
        sys.exit(
            "cloudflared not found. Install it:\n"
            "  Windows:  winget install Cloudflare.cloudflared\n"
            "  macOS:    brew install cloudflared"
        )
    return found


def main() -> None:
    token = _get_or_create_token()
    cf = _find_cloudflared()
    py = HERE / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    port = os.environ.get("HIVEMIND_HTTP_PORT", "8765")

    print(f"[1/2] Starting hivemind HTTP server on 127.0.0.1:{port} ...")
    server = subprocess.Popen([str(py), str(HERE / "mcp_http.py")])
    time.sleep(3)
    if server.poll() is not None:
        sys.exit("HTTP server exited immediately — check mcp_http.py / .env.")

    print("[2/2] Opening cloudflared tunnel ...")
    tunnel = subprocess.Popen(
        [str(cf), "tunnel", "--url", f"http://127.0.0.1:{port}", "--no-autoupdate"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1,
    )

    public = None
    for line in tunnel.stdout:  # type: ignore[union-attr]
        m = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", line)
        if m:
            public = m.group(0)
            break

    if not public:
        server.terminate()
        sys.exit("Could not obtain a tunnel URL. Is cloudflared blocked by a firewall?")

    url = f"{public}/mcp-{token}"
    (HERE / "CONNECTOR_URL.txt").write_text(url + "\n", encoding="utf-8")

    bar = "=" * 72
    print("\n" + bar)
    print("PASTE THIS as the 'Remote MCP server URL' in Add custom connector:")
    print("\n    " + url + "\n")
    print("(also saved to CONNECTOR_URL.txt)")
    print(bar)
    print("Leave this window OPEN while using the hivemind in Cowork / chat.")
    print("Press Ctrl+C to stop the server and tunnel.\n")

    try:
        tunnel.wait()
    except KeyboardInterrupt:
        pass
    finally:
        tunnel.terminate()
        server.terminate()
        print("\nStopped hivemind server and tunnel.")


if __name__ == "__main__":
    main()
