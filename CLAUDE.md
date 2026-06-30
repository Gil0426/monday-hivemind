# CLAUDE.md — Rules for Maintainers and Claude Code

This file governs how Claude Code (and human maintainers) should work in this repo.

---

## The folder-per-specialist pattern

Every specialist lives in `specialists/<name>/` with exactly two files:

- **`persona.md`** — the specialist's identity, area of expertise, step-by-step approach,
  and hard constraints (what monday.com does NOT support in this domain).
- **`reference.md`** — the grounding document: real monday.com column type IDs, board
  structures in tables, status label JSON configs, and documented limitations.
  Every claim must be traceable to https://support.monday.com or https://developer.monday.com.

The Manager discovers specialists by scanning this folder at runtime. No registration step needed.

---

## Grounding rules — never violate these

1. **Always cite monday.com documentation.** If a column type, feature, or behavior is
   mentioned in a specialist's reference.md, it must have come from official monday.com docs.
   Do not copy from memory alone — verify against the source.

2. **Never invent capabilities.** If monday.com does not support a feature
   (e.g., cross-board formula columns, required fields, native email sending), say so explicitly
   and document it under "Limitations" in the relevant reference.md.

3. **Dry-run is the default.** `shared/monday_tools.py` has `DRY_RUN = True`. Do not flip it
   to False without a deliberate decision and a live API integration in place.

4. **Specialists do not call automations.** monday.com automations are configured separately
   by the end user. Board design does not include automation setup. Never promise automation
   behavior in a board plan.

---

## What Claude Code must never do in this repo

- **Never edit `shared/`** without explicit instruction from the repo owner.
  The `shared/` engine is the stable foundation all specialists depend on.
  Breaking it breaks everything.

- **Never add imports or dependencies to `shared/`** without updating `requirements.txt`
  and noting the addition in a commit message.

- **Never write a specialist reference.md from memory alone.** Always note where the
  information came from. If uncertain, search https://support.monday.com first and quote
  the relevant section.

- **Never commit `.env`** — it contains the API key. `.env.example` is the only env file
  that belongs in git.

- **Never write Monday API calls that execute in production** unless `DRY_RUN = False`
  is intentionally set and the change is reviewed.

---

## Adding a new specialist — checklist

- [ ] Created `specialists/<name>/persona.md` with: identity, approach, hard constraints
- [ ] Created `specialists/<name>/reference.md` with: column types table, board structure
      examples, status label JSON, limitations section
- [ ] Every claim in reference.md is traceable to official monday.com docs
- [ ] The Manager picks up the specialist on next run (no code change needed)
- [ ] Committed `specialists/<name>/` to the repo

---

## Modifying the engine (`shared/`)

Changes to `shared/` affect every specialist. Before editing:

1. Discuss with teammates first — at minimum, leave a comment in the PR.
2. Run the smoke test: `python -c "from shared.tool_registry import get_specialist_tools; from shared.monday_tools import BuildPlan; print(get_specialist_tools(BuildPlan()))"` must succeed.
3. Do not change the public API of `agent_loop.run()` without updating the Manager.

---

## Commit message convention

```
feat(specialists): add marketing specialist
fix(shared): handle missing persona.md gracefully
docs(crm): add limitations for board_relation column
```
