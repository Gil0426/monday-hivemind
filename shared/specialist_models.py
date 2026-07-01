"""
shared/specialist_models.py

Per-specialist model assignment for board-design runs. The agent loop looks up
a specialist's model by folder name here; anything not listed (e.g. a freshly
created specialist) falls back to DEFAULT_MODEL.

Not every specialist needs the top model — match the model to the job:
give complex, multi-board designers the strongest model and let simple,
mechanical specialists run on the fast/cheap one. To retune, just edit MODELS
below; no other code changes needed. Routing (which specialist handles a
request) is a separate, always-cheap Haiku call and is unaffected.
"""

from __future__ import annotations

# Model tiers
OPUS = "claude-opus-4-8"                 # top quality — multi-board, nuanced design
SONNET = "claude-sonnet-5"               # strong default for real design work
HAIKU = "claude-haiku-4-5-20251001"      # fast/cheap — simple, mechanical boards

# Default for any specialist not in MODELS (including newly created ones).
DEFAULT_MODEL = SONNET

# Per-specialist overrides. Add your own specialists here; anything omitted
# uses DEFAULT_MODEL.
MODELS: dict[str, str] = {
    # High complexity → Opus (multi-board, nuanced structure)
    "crm": OPUS,
    "project-management": OPUS,
    # Medium complexity → Sonnet (real design work)
    "analytics-dashboards": SONNET,
    "operational-dashboards": SONNET,
    "example-board-builder": SONNET,
    "automation-specialist": SONNET,
    "ai-tools": SONNET,
    "validation": SONNET,
    "monday-ai": SONNET,
    # Low complexity → Haiku (simple, mechanical single-board output)
    "action-items": HAIKU,
    "data-import": HAIKU,
    "documentation": HAIKU,
}


def model_for(name: str) -> str:
    """Return the model id for a specialist folder name, or DEFAULT_MODEL if unset."""
    return MODELS.get(name, DEFAULT_MODEL)
