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
from shared.specialist_models import model_for

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


_MODEL_LABELS = {
    "claude-opus-4-8": "Opus 4.8",
    "claude-sonnet-5": "Sonnet 5",
    "claude-haiku-4-5-20251001": "Haiku 4.5",
}


def _model_label(name: str) -> str:
    """Short, human-readable model name for a specialist (from specialist_models.model_for)."""
    return _MODEL_LABELS.get(model_for(name), model_for(name))


@mcp.tool()
def list_specialists() -> str:
    """List all monday.com board-building specialists, their domains, and the model each uses.

    The model shown is the one that specialist actually runs on for board design
    (set in shared/specialist_models.py) — not every specialist uses the same model.
    """
    dirs = _find_dirs()
    if not dirs:
        return "No specialists found. Use create_specialist to add one."
    lines = ["Available specialists (model = what each uses for board design):\n"]
    for d in dirs:
        lines.append(f"  • {d.name:<24} [{_model_label(d.name):<9}] {_tagline(d)}")
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
def create_specialist(
    name: str,
    purpose: str,
    primary_users: str,
    core_workflows: str,
    key_boards_and_objects: str,
    critical_columns: str,
    known_limitations: str = "",
) -> str:
    """
    Create a new monday.com board-building specialist — only after gathering real
    requirements. A specialist is only useful if it reflects how the team actually
    works, so this tool REQUIRES that context up front instead of improvising it.

    ASSISTANT INSTRUCTIONS — READ BEFORE CALLING:
    Do NOT call this tool with guessed or invented values. First interview the user
    and fill every field from their answers. For any field the user hasn't given you,
    ask a specific, concrete question (e.g. "Who will use these boards day to day?",
    "What are the must-have columns and what should each track?"). Ask about all
    missing fields in one turn so it's quick. If the user genuinely doesn't know a
    field, record what they said (e.g. "user unsure — confirm later") rather than
    fabricating monday.com capabilities. Ground everything in real monday.com features
    (https://support.monday.com, https://developer.monday.com).

    Args:
        name:                   Folder slug for the specialist (e.g. 'marketing', 'service-desk').
        purpose:                What this specialist is for and when to route requests to it (1–2 sentences).
        primary_users:          Who uses these boards and their roles (e.g. 'SDRs plus one sales manager').
        core_workflows:         The main processes the boards must support, described step by step.
        key_boards_and_objects: What's tracked and how it's structured — single board vs. multiple connected
                                boards, and the main items/entities on each.
        critical_columns:       Must-have columns and their monday.com column types
                                (e.g. 'Stage (status), Value (numbers), Owner (people), Close date (date)').
        known_limitations:      monday.com limits in this domain to respect (optional; leave blank if none known).
    """
    slug = name.lower().replace(" ", "-")
    target = SPECIALISTS_DIR / slug

    if target.exists():
        return f"Specialist '{slug}' already exists at specialists/{slug}/"

    requirements = (
        f"- Purpose / when to route here: {purpose}\n"
        f"- Primary users: {primary_users}\n"
        f"- Core workflows: {core_workflows}\n"
        f"- Boards & objects: {key_boards_and_objects}\n"
        f"- Critical columns: {critical_columns}\n"
        f"- Known limitations: {known_limitations or '(none provided)'}"
    )

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": (
                f"Create files for a monday.com board-building specialist named '{slug}'.\n"
                f"Use ONLY the requirements below. Do not invent capabilities — ground every "
                f"column type, feature, and limitation in real monday.com behavior. If something "
                f"in the requirements isn't possible in monday.com, say so under Limitations.\n\n"
                f"Requirements gathered from the user:\n{requirements}\n\n"
                f"Output EXACTLY this format:\n\n"
                f"===PERSONA_START===\n"
                f"[persona.md: identity; the specific domain and when to use this specialist; a "
                f"step-by-step approach tuned to the workflows above; and hard constraints — what "
                f"monday.com does NOT support in this domain]\n"
                f"===PERSONA_END===\n\n"
                f"===REFERENCE_START===\n"
                f"[reference.md: a column types table (column name → monday.com column type → why "
                f"it's used here); the board structure (groups/columns, single vs. multi-board); "
                f"example status label configurations as JSON; and a Limitations section. Every "
                f"claim must reflect real monday.com capabilities.]\n"
                f"===REFERENCE_END==="
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
        f"✓ Specialist '{slug}' created from your requirements:\n"
        f"  specialists/{slug}/persona.md\n"
        f"  specialists/{slug}/reference.md\n\n"
        f"It runs on {_model_label(slug)} for board design (default for new specialists; "
        f"change it in shared/specialist_models.py).\n"
        f"To keep it: git add specialists/{slug}/ && git commit -m 'feat: add {slug} specialist', "
        f"then redeploy so it's live remotely."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
