#!/usr/bin/env python3
"""
manager/manager.py — monday.com Hivemind Manager

The single user-facing interface. Lists specialists, routes build requests to the
right one, and can generate new specialists on demand (saved to disk for teammates).

Run from monday-hivemind/:
    python -m manager.manager
"""

from __future__ import annotations
import pathlib
import sys

import anthropic

from shared.agent_loop import load_specialist, run as run_specialist, MODEL

SPECIALISTS_DIR = pathlib.Path(__file__).parent.parent / "specialists"

ROUTER_MODEL = "claude-haiku-4-5-20251001"   # fast model — only picks a name
BUILDER_MODEL = MODEL                         # full model — generates specialist files

BANNER = """\
╔══════════════════════════════════════════════════════╗
║         monday.com HIVEMIND  ·  Manager              ║
║   Board design grounded in real monday.com docs      ║
╚══════════════════════════════════════════════════════╝"""

HELP = """\
Commands:
  build <request>                  describe the board you want
  build --doc <path> <request>     attach a requirements document
  new specialist                   generate and save a new specialist
  list                             show available specialists
  help                             show this menu
  quit / exit                      exit
"""


# ---------------------------------------------------------------------------
# Specialist discovery
# ---------------------------------------------------------------------------

def _find_specialists() -> list[pathlib.Path]:
    if not SPECIALISTS_DIR.exists():
        return []
    return sorted(
        d for d in SPECIALISTS_DIR.iterdir()
        if d.is_dir()
        and (d / "persona.md").exists()
        and (d / "reference.md").exists()
    )


def _tagline(specialist_dir: pathlib.Path) -> str:
    for line in (specialist_dir / "persona.md").read_text(encoding="utf-8").splitlines():
        line = line.strip().lstrip("#").strip()
        if line and not line.lower().startswith("specialist:"):
            return line[:65]
    return ""


def _show_specialists(dirs: list[pathlib.Path]) -> None:
    print("\nAvailable specialists:")
    for d in dirs:
        print(f"  {d.name:<30}  {_tagline(d)}")
    print()


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------

def _route(user_message: str, dirs: list[pathlib.Path]) -> pathlib.Path:
    """Use a fast Claude call to pick the best specialist."""
    if len(dirs) == 1:
        return dirs[0]

    names = "\n".join(f"- {d.name}" for d in dirs)
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=ROUTER_MODEL,
        max_tokens=30,
        messages=[{
            "role": "user",
            "content": (
                f"Pick the best specialist folder name for this monday.com board request.\n"
                f"Available:\n{names}\n\n"
                f"Request: {user_message}\n\n"
                f"Reply with ONLY the exact folder name, nothing else."
            ),
        }],
    )
    chosen = response.content[0].text.strip().lower().strip("-").strip()

    # exact match first
    for d in dirs:
        if d.name == chosen:
            return d
    # partial match fallback
    for d in dirs:
        if d.name in chosen or chosen in d.name:
            return d
    return dirs[0]


# ---------------------------------------------------------------------------
# Specialist creation
# ---------------------------------------------------------------------------

def _create_specialist() -> None:
    """Interactively generate persona.md + reference.md for a new specialist and save to disk."""
    raw_name = input("\n  Specialist name (slug, e.g. 'marketing' or 'service-desk'): ").strip()
    slug = raw_name.lower().replace(" ", "-")
    if not slug:
        print("  Cancelled.\n")
        return

    target = SPECIALISTS_DIR / slug
    if target.exists():
        print(f"  Specialist '{slug}' already exists at {target}\n")
        return

    domain = input(
        f"  Describe what '{slug}' covers\n"
        f"  (board types, use case, example columns): "
    ).strip()
    if not domain:
        print("  Cancelled.\n")
        return

    print(f"\n  Generating '{slug}'...")

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=BUILDER_MODEL,
        max_tokens=4000,
        messages=[{
            "role": "user",
            "content": (
                f"Generate files for a new monday.com board-building specialist.\n\n"
                f"Specialist name: {slug}\n"
                f"Domain: {domain}\n\n"
                f"Output EXACTLY this format with these delimiters on their own lines:\n\n"
                f"===PERSONA_START===\n"
                f"[persona.md content]\n"
                f"===PERSONA_END===\n\n"
                f"===REFERENCE_START===\n"
                f"[reference.md content]\n"
                f"===REFERENCE_END===\n\n"
                f"persona.md must cover: specialist identity, domain expertise, "
                f"step-by-step approach to board design, and hard constraints "
                f"(what monday.com does NOT support in this domain).\n\n"
                f"reference.md must cover: relevant monday.com column types with type IDs, "
                f"typical board structures (groups, columns) in a table, status label "
                f"configurations, and documented limitations. Ground everything in real "
                f"monday.com capabilities — never invent features."
            ),
        }],
    )

    text = response.content[0].text
    try:
        persona = text.split("===PERSONA_START===")[1].split("===PERSONA_END===")[0].strip()
        reference = text.split("===REFERENCE_START===")[1].split("===REFERENCE_END===")[0].strip()
    except IndexError:
        print("  ERROR: Could not parse generated output. Try again.\n")
        return

    target.mkdir(parents=True)
    (target / "persona.md").write_text(persona + "\n", encoding="utf-8")
    (target / "reference.md").write_text(reference + "\n", encoding="utf-8")

    print(f"\n  ✓  specialists/{slug}/persona.md")
    print(f"  ✓  specialists/{slug}/reference.md")
    print(f"\n  Specialist '{slug}' is ready.")
    print(f"  Commit specialists/{slug}/ to share it with your team.\n")


# ---------------------------------------------------------------------------
# Main REPL
# ---------------------------------------------------------------------------

def main() -> None:
    print(BANNER)
    print()

    dirs = _find_specialists()
    if not dirs:
        print("No specialists found in specialists/.")
        print("Run the manager and type: new specialist\n")
        sys.exit(1)

    _show_specialists(dirs)
    print(HELP)

    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not raw:
            continue

        low = raw.lower()

        if low in ("quit", "exit", "q"):
            print("Bye.")
            break

        if low in ("help", "h", "?"):
            print(HELP)
            continue

        if low == "list":
            dirs = _find_specialists()
            _show_specialists(dirs)
            continue

        if low == "new specialist":
            _create_specialist()
            dirs = _find_specialists()
            continue

        if low.startswith("build"):
            rest = raw[len("build"):].strip()

            document_path: str | None = None
            if rest.startswith("--doc"):
                parts = rest[len("--doc"):].strip().split(None, 1)
                if len(parts) < 2:
                    print("  Usage: build --doc <path> <your request>\n")
                    continue
                document_path, rest = parts[0], parts[1]

            if not rest:
                print("  Please describe what board you want.\n")
                continue

            dirs = _find_specialists()
            chosen = _route(rest, dirs)
            print(f"\n  → Routing to: {chosen.name}\n")

            specialist = load_specialist(chosen)
            result = run_specialist(
                specialist,
                rest,
                document_path=document_path,
                verbose=False,
            )
            print(result)
            print()
            continue

        print(f"  Unknown command '{raw}'. Type 'help' for options.\n")


if __name__ == "__main__":
    main()
