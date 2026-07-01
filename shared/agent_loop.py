"""
shared/agent_loop.py

The reusable agentic loop that powers every specialist.
Loads a specialist from its folder, injects persona + reference into the
system prompt, then runs the standard Anthropic tool-use loop until the
model reaches end_turn.
"""

from __future__ import annotations
import pathlib
from dataclasses import dataclass
from typing import Any

import anthropic

from shared.monday_tools import BuildPlan
from shared.tool_registry import get_specialist_tools
from shared.specialist_models import model_for


# Default/builder model. Per-specialist board-design models live in
# shared/specialist_models.py (see model_for). This constant is kept for the
# specialist-file *generation* step in mcp_server.py / manager.py.
MODEL = "claude-opus-4-8"
MAX_TOKENS = 4096


# ---------------------------------------------------------------------------
# Specialist data object
# ---------------------------------------------------------------------------

@dataclass
class Specialist:
    name: str
    persona: str     # full text of persona.md
    reference: str   # full text of reference.md


def load_specialist(specialist_dir: str | pathlib.Path) -> Specialist:
    """Load a specialist from its folder. Raises FileNotFoundError if files are missing."""
    d = pathlib.Path(specialist_dir)
    persona_path = d / "persona.md"
    reference_path = d / "reference.md"

    if not persona_path.exists():
        raise FileNotFoundError(f"Missing persona.md in {d}")
    if not reference_path.exists():
        raise FileNotFoundError(f"Missing reference.md in {d}")

    return Specialist(
        name=d.name,
        persona=persona_path.read_text(encoding="utf-8").strip(),
        reference=reference_path.read_text(encoding="utf-8").strip(),
    )


# ---------------------------------------------------------------------------
# System prompt assembly
# ---------------------------------------------------------------------------

def _build_system_prompt(specialist: Specialist) -> str:
    return f"""\
{specialist.persona}

---

## YOUR REFERENCE DOCUMENT

The following is your primary grounding document. You MUST consult it before designing
any board. If the user's request requires knowledge not covered here, search official
monday.com documentation (https://support.monday.com or https://developer.monday.com).

NEVER invent column types, features, or behaviors that are not documented in monday.com.
If unsure, say so and cite where the user can verify.

{specialist.reference}

---

## TOOL USAGE RULES

- read_document   → call first if the user provides a file path describing requirements.
- create_board    → start every board design here; note the returned board_id.
- create_group    → add groups before columns or items.
- create_column   → add all columns using valid monday.com type IDs.
- create_item     → add 1–3 realistic sample items per group to illustrate usage.
- show_build_plan → ALWAYS call this last to present the complete plan to the user.

All operations are DRY-RUN. Nothing is written to monday.com.
"""


# ---------------------------------------------------------------------------
# Agent loop
# ---------------------------------------------------------------------------

def run(
    specialist: Specialist,
    user_message: str,
    document_path: str | None = None,
    *,
    verbose: bool = False,
) -> str:
    """
    Run the agentic loop for one specialist turn.
    Returns the specialist's final text response (after all tool calls complete).
    """
    client = anthropic.Anthropic()
    plan = BuildPlan()
    tool_defs, handlers = get_specialist_tools(plan)
    system = _build_system_prompt(specialist)
    model = model_for(specialist.name)

    # If a document was uploaded, ask the specialist to read it first
    if document_path:
        first_message = (
            f"The user has provided a document at: {document_path}\n"
            f"Please read it with read_document, then answer their request.\n\n"
            f"User request: {user_message}"
        )
    else:
        first_message = user_message

    messages: list[dict[str, Any]] = [{"role": "user", "content": first_message}]

    while True:
        response = client.messages.create(
            model=model,
            max_tokens=MAX_TOKENS,
            system=system,
            tools=tool_defs,
            messages=messages,
        )

        if verbose:
            print(f"  [loop] stop_reason={response.stop_reason}  blocks={len(response.content)}")

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            return "\n".join(
                block.text
                for block in response.content
                if hasattr(block, "text") and block.text
            )

        if response.stop_reason != "tool_use":
            return f"[agent_loop] Unexpected stop_reason: {response.stop_reason}"

        # Execute tool calls and collect results
        tool_results: list[dict[str, Any]] = []
        for block in response.content:
            if block.type != "tool_use":
                continue

            handler = handlers.get(block.name)
            if handler is None:
                result = f"ERROR: Unknown tool '{block.name}'"
            else:
                try:
                    result = handler(block.input)
                except Exception as exc:
                    result = f"ERROR executing {block.name}: {exc}"

            if verbose:
                preview = result[:100].replace("\n", " ")
                print(f"  [tool] {block.name} → {preview}")

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result,
            })

        messages.append({"role": "user", "content": tool_results})
