#!/usr/bin/env python3
"""
mcp_server.py — monday-hivemind MCP server

Exposes board-design tools to the Claude desktop and web apps via the
Model Context Protocol. Claude can call these tools directly in chat —
no terminal required.

Registration: see README.md → "Use from Claude app"
"""

from __future__ import annotations
import os
import pathlib
import sys

# ── Bootstrap: load .env and fix import path before any project imports ──────

_HERE = pathlib.Path(__file__).parent.resolve()

_env = _HERE / ".env"
if _env.exists():
    for _line in _env.read_text(encoding="utf-8").splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _, _v = _line.partition("=")
            os.environ.setdefault(_k.strip(), _v.strip())

sys.path.insert(0, str(_HERE))

# ── Imports ───────────────────────────────────────────────────────────────────

import anthropic
from mcp.server.fastmcp import FastMCP

from shared.agent_loop import load_specialist, run as run_specialist, MODEL

# ── Specialist helpers (self-contained; avoids manager.py path assumptions) ───

SPECIALISTS_DIR = _HERE / "specialists"


def _find_dirs() -> list[pathlib.Path]:
    if not SPECIALISTS_DIR.exists():
        return []
    return sorted(
        d for d in SPECIALISTS_DIR.iterdir()
        if d.is_dir()
        and (d / "persona.md").exists()
        and (d / "reference.md").exists()
    )


def _tagline(d: pathlib.Path) -> str:
    for line in (d / "persona.md").read_text(encoding="utf-8").splitlines():
        line = line.strip().lstrip("#").strip()
        if line and not line.lower().startswith("specialist:"):
            return line[:80]
    return ""


def _route(description: str, dirs: list[pathlib.Path]) -> pathlib.Path:
    if len(dirs) == 1:
        return dirs[0]
    names = "\n".join(f"- {d.name}" for d in dirs)
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=30,
        messages=[{
            "role": "user",
            "content": (
                f"Pick the best specialist folder name for this monday.com board request.\n"
                f"Available:\n{names}\n\nRequest: {description}\n\n"
                f"Reply with ONLY the exact folder name, nothing else."
            ),
        }],
    )
    chosen = resp.content[0].text.strip().lower()
    for d in dirs:
        if d.name == chosen or d.name in chosen:
            return d
    return dirs[0]


# ── MCP server ────────────────────────────────────────────────────────────────

mcp = FastMCP(
    "monday-hivemind",
    instructions=(
        "You have access to a team of monday.com board-building specialists. "
        "Use design_board to create a complete dry-run board plan from a description. "
        "Use list_specialists to see available domains. "
        "Use create_specialist to add a new domain expert on the fly."
    ),
)


@mcp.tool()
def list_specialists() -> str:
    """List all available monday.com board-building specialists and their domains."""
    dirs = _find_dirs()
    if not dirs:
        return "No specialists found. Use create_specialist to add one."
    lines = ["Available specialists:\n"]
    for d in dirs:
        lines.append(f"  • {d.name:<30} {_tagline(d)}")
    return "\n".join(lines)


@mcp.tool()
def design_board(
    description: str,
    specialist: str | None = None,
    document_path: str | None = None,
) -> str:
    """
    Design a monday.com board and return a complete dry-run build plan.

    The plan includes every board, group, column, and sample item that would be
    created — nothing is written to monday.com until you approve it.

    Args:
        description:   What the board should track or accomplish. Be as specific as you like.
        specialist:    Optional specialist to use (e.g. 'crm', 'project-management').
                       Omit to let the system route automatically.
        document_path: Optional path to a .txt or .pdf requirements document in inputs/.
    """
    dirs = _find_dirs()
    if not dirs:
        return "No specialists found. Use create_specialist first."

    if specialist:
        chosen = next((d for d in dirs if d.name == specialist), None)
        if chosen is None:
            available = ", ".join(d.name for d in dirs)
            return f"Specialist '{specialist}' not found. Available: {available}"
    else:
        chosen = _route(description, dirs)

    loaded = load_specialist(chosen)
    return run_specialist(loaded, description, document_path=document_path)


@mcp.tool()
def create_specialist(name: str, domain: str) -> str:
    """
    Generate and save a new specialist to the specialists/ folder.
    The specialist is immediately available and can be committed to the shared git repo.

    Args:
        name:   Folder slug for the new specialist (e.g. 'marketing', 'service-desk').
        domain: What boards this specialist covers — be descriptive, this becomes its reference doc.
    """
    slug = name.lower().replace(" ", "-")
    target = SPECIALISTS_DIR / slug

    if target.exists():
        return f"Specialist '{slug}' already exists at specialists/{slug}/"

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": (
                f"Generate files for a new monday.com board-building specialist.\n\n"
                f"Specialist name: {slug}\nDomain: {domain}\n\n"
                f"Output EXACTLY this format:\n\n"
                f"===PERSONA_START===\n"
                f"[persona.md: identity, approach, hard constraints for this domain]\n"
                f"===PERSONA_END===\n\n"
                f"===REFERENCE_START===\n"
                f"[reference.md: column types table with type IDs, board structures, "
                f"status label JSON, limitations section]\n"
                f"===REFERENCE_END===\n\n"
                f"Ground everything in real monday.com capabilities. Never invent features."
            ),
        }],
    )

    text = response.content[0].text
    try:
        persona = text.split("===PERSONA_START===")[1].split("===PERSONA_END===")[0].strip()
        reference = text.split("===REFERENCE_START===")[1].split("===REFERENCE_END===")[0].strip()
    except IndexError:
        return "ERROR: Could not parse generated output. Please try again."

    target.mkdir(parents=True)
    (target / "persona.md").write_text(persona + "\n", encoding="utf-8")
    (target / "reference.md").write_text(reference + "\n", encoding="utf-8")

    return (
        f"✓ Specialist '{slug}' created:\n"
        f"  specialists/{slug}/persona.md\n"
        f"  specialists/{slug}/reference.md\n\n"
        f"Run: git add specialists/{slug}/ && git commit -m 'feat: add {slug} specialist'"
        f" to share with your team."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
