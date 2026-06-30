"""
shared/monday_tools.py

Board-building tools for monday.com specialists.
All operations are DRY-RUN by default — they accumulate a BuildPlan and
print a preview. No changes are made to monday.com until DRY_RUN = False
and a live API integration is wired in.
"""

from __future__ import annotations
import json
from dataclasses import dataclass, field
from typing import Any


DRY_RUN = True  # flip to False only when live API is wired up


# ---------------------------------------------------------------------------
# Build plan accumulator
# ---------------------------------------------------------------------------

@dataclass
class _Op:
    kind: str
    params: dict[str, Any]
    fake_id: str


@dataclass
class BuildPlan:
    ops: list[_Op] = field(default_factory=list)
    _counters: dict[str, int] = field(default_factory=dict)

    def _next_id(self, kind: str) -> str:
        n = self._counters.get(kind, 0) + 1
        self._counters[kind] = n
        return f"{kind}_{n}"

    def add(self, kind: str, params: dict[str, Any]) -> str:
        fake_id = self._next_id(kind)
        self.ops.append(_Op(kind=kind, params=params, fake_id=fake_id))
        return fake_id

    def summary(self) -> str:
        if not self.ops:
            return "Build plan is empty — no operations recorded yet."

        lines = ["╔══════════════════════════════════════╗",
                 "║    BOARD BUILD PLAN  (DRY-RUN)       ║",
                 "╚══════════════════════════════════════╝", ""]

        for op in self.ops:
            lines.append(f"  [{op.fake_id}]  {op.kind.upper()}")
            for k, v in op.params.items():
                if v or v == 0:
                    lines.append(f"      {k}: {json.dumps(v, ensure_ascii=False)}")
            lines.append("")

        lines.append("─" * 40)
        lines.append("No changes made — this is a preview only.")
        lines.append("Run with DRY_RUN=False to build for real.")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Tool definitions (Anthropic tool-use schema)
# ---------------------------------------------------------------------------

TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "name": "create_board",
        "description": (
            "Register a new monday.com board in the build plan. "
            "Returns a board_id to reference in subsequent calls."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Board name as it will appear in monday.com.",
                },
                "board_kind": {
                    "type": "string",
                    "enum": ["public", "private", "share"],
                    "description": "public = visible to workspace; private = invite-only; share = external shareable.",
                },
                "description": {
                    "type": "string",
                    "description": "Optional board description shown in the board header.",
                },
            },
            "required": ["name", "board_kind"],
        },
    },
    {
        "name": "create_group",
        "description": (
            "Add a group (section) to a board in the build plan. "
            "Groups organize items into rows with a shared header."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "board_id": {
                    "type": "string",
                    "description": "board_id returned by create_board.",
                },
                "name": {
                    "type": "string",
                    "description": "Group label (e.g. 'To Do', 'In Progress', 'Done').",
                },
                "color": {
                    "type": "string",
                    "description": "Optional hex color for the group header (e.g. '#ff6b6b').",
                },
            },
            "required": ["board_id", "name"],
        },
    },
    {
        "name": "create_column",
        "description": (
            "Add a column to a board in the build plan. "
            "Use official monday.com column type IDs: "
            "text, numbers, status, date, people, timeline, checkbox, dropdown, "
            "email, phone, link, long_text, rating, dependency, board_relation, "
            "formula, tags, location, file, time_tracking, world_clock, color_picker, "
            "item_id, auto_number, creation_log, last_updated, week, country."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "board_id": {
                    "type": "string",
                    "description": "board_id returned by create_board.",
                },
                "title": {
                    "type": "string",
                    "description": "Column header label visible to users.",
                },
                "column_type": {
                    "type": "string",
                    "description": "monday.com column type ID (see tool description for valid values).",
                },
                "settings": {
                    "type": "object",
                    "description": (
                        "Type-specific settings object. "
                        "For status: {labels: {0: 'Not Started', 1: 'In Progress', 2: 'Done'}}. "
                        "For dropdown: {settings: {labels: [{name: 'Option A'}, {name: 'Option B'}]}}."
                    ),
                },
            },
            "required": ["board_id", "title", "column_type"],
        },
    },
    {
        "name": "create_item",
        "description": (
            "Add a sample item (row) to a group in the build plan. "
            "Use this to populate realistic example data that shows the board's intended use."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "board_id": {
                    "type": "string",
                    "description": "board_id returned by create_board.",
                },
                "group_id": {
                    "type": "string",
                    "description": "group_id returned by create_group.",
                },
                "item_name": {
                    "type": "string",
                    "description": "Item name (the value in the Name/Title column).",
                },
                "column_values": {
                    "type": "object",
                    "description": "Map of column title to example value for this item.",
                },
            },
            "required": ["board_id", "group_id", "item_name"],
        },
    },
    {
        "name": "show_build_plan",
        "description": (
            "Return the complete dry-run build plan accumulated so far as a formatted string. "
            "Always call this at the end of every board design session so the user sees the full plan."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]


# ---------------------------------------------------------------------------
# Handler factory — closures bind each handler to the shared BuildPlan
# ---------------------------------------------------------------------------

def make_handlers(plan: BuildPlan) -> dict[str, Any]:
    """Return a tool-name → handler map bound to `plan`."""

    def _create_board(args: dict[str, Any]) -> str:
        board_id = plan.add("board", {
            "name": args["name"],
            "board_kind": args["board_kind"],
            "description": args.get("description", ""),
        })
        return json.dumps({"board_id": board_id, "dry_run": True})

    def _create_group(args: dict[str, Any]) -> str:
        group_id = plan.add("group", {
            "board_id": args["board_id"],
            "name": args["name"],
            "color": args.get("color", ""),
        })
        return json.dumps({"group_id": group_id, "dry_run": True})

    def _create_column(args: dict[str, Any]) -> str:
        col_id = plan.add("column", {
            "board_id": args["board_id"],
            "title": args["title"],
            "column_type": args["column_type"],
            "settings": args.get("settings", {}),
        })
        return json.dumps({"column_id": col_id, "dry_run": True})

    def _create_item(args: dict[str, Any]) -> str:
        item_id = plan.add("item", {
            "board_id": args["board_id"],
            "group_id": args["group_id"],
            "item_name": args["item_name"],
            "column_values": args.get("column_values", {}),
        })
        return json.dumps({"item_id": item_id, "dry_run": True})

    def _show_build_plan(_args: dict[str, Any]) -> str:
        return plan.summary()

    return {
        "create_board": _create_board,
        "create_group": _create_group,
        "create_column": _create_column,
        "create_item": _create_item,
        "show_build_plan": _show_build_plan,
    }
