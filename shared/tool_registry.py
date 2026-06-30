"""
shared/tool_registry.py

Assembles the tool set that specialists receive.
Specialists always get: document reader + all board-building tools.
The registry is the single place to add new shared tools.
"""

from __future__ import annotations
from typing import Any, Callable

import shared.document_reader as _dr
from shared.monday_tools import TOOL_DEFINITIONS as _MONDAY_DEFS, BuildPlan, make_handlers


ToolDef = dict[str, Any]
Handler = Callable[[dict[str, Any]], str]


def get_specialist_tools(plan: BuildPlan) -> tuple[list[ToolDef], dict[str, Handler]]:
    """
    Return (tool_definitions, handler_map) for a specialist agent.

    tool_definitions — list of Anthropic tool schemas passed to the API
    handler_map      — tool name → callable that executes the tool
    """
    defs: list[ToolDef] = [_dr.TOOL_DEFINITION] + _MONDAY_DEFS
    handlers: dict[str, Handler] = {"read_document": _dr.handle}
    handlers.update(make_handlers(plan))
    return defs, handlers
