# action-items — Reference

This specialist produces no boards and writes no API calls. This reference exists so you can (a) recognize what upstream specialists were manipulating, and (b) correctly attribute manual-step and platform-limit action items to real monday.com features. Never invent capabilities that aren't listed here.

## Column Types (for recognizing upstream references)

Use these type IDs to identify which column an upstream artifact is talking about when you phrase an action item.

| Column | API type ID | Notes for action items |
|---|---|---|
| Status | `status` | Labels + colors set via API; some label edits are UI-only nuisance. |
| Dropdown | `dropdown` | Multi-select labels. |
| Text | `text` | Plain single-line text. |
| Long Text | `long_text` | Multi-line; "reflection" / notes columns often here. |
| Numbers | `numbers` | |
| People | `people` | Assignment; may need manual re-assign after build. |
| Date | `date` | Automation date offsets (e.g. +1 day) often must be set in UI. |
| Timeline | `timeline` | Start/end range. |
| Tags | `tags` | Shared across boards. |
| Email | `email` | Mailbox/outbound integrations are UI-wired. |
| Phone | `phone` | |
| Link | `link` | |
| Checkbox | `checkbox` | |
| Rating | `rating` | |
| Formula | `formula` | Formula body frequently must be typed in the UI, not API. |
| Mirror | `mirror` | Requires an existing connect-boards column; often manual. |
| Connect Boards | `board_relation` | Board linking; sometimes UI-completed. |
| Dependency | `dependency` | Needs dependency-aware columns. |
| Time Tracking | `time_tracking` | |
| Item ID | `item_id` | Read-only. |
| Creation Log | `creation_log` | Read-only. |
| Last Updated | `last_updated` | Read-only. |
| Country | `country` | |
| Location | `location` | |
| Vote | `vote` | |
| World Clock | `world_clock` | |
| Week | `week` | |
| Hour | `hour` | |

## Board Structures (for attribution)

When attributing an action item, name the structure it belongs to:
- **Board** — top-level container. May be `public`, `private`, or `shareable`.
- **Group** — colored row section within a board.
- **Item** — a row; **Subitem** — nested row (uses a hidden subitems board).
- **Column** — typed field (see table above).
- **View** — Table, Kanban, Calendar, Timeline/Gantt, Chart, Form, Cards, Workload. Some views (e.g. filtered "Today" tables) are typically added in the UI.
- **Dashboard** — cross-board widget container; widgets are UI-configured.
- **Automation** — recipe (trigger → action); many parameters (date offsets, specific people) are UI-only.
- **Integration** — external connection (email/mailbox, Slack, etc.); credential wiring is UI-only.

## Status Label JSON (shape reference)

Upstream status columns are defined with a labels map. You only need to recognize this shape when a defect references a wrong or missing label:

```json
{
  "labels": {
    "0": "Not Started",
    "1": "Working on it",
    "2": "Stuck",
    "3": "Done"
  },
  "labels_colors": {
    "0": { "color": "#c4c4c4" },
    "1": { "color": "#fdab3d" },
    "2": { "color": "#e2445c" },
    "3": { "color": "#00c875" }
  }
}
```

An action item might be: `- [ ] Rename status label index 2 from "Stuck" to "Blocked" (validation: PARTIAL)`.

## Common Manual-Step / Platform-Limit Sources

These are the recurring reasons an item lands under `### Blocked / platform limits` or `### Consultant (in monday)`. Ground your attributions in these real limits — do not invent new ones.

- **Automation date offsets** (e.g. "+1 day", "+3 business days") frequently cannot be fully set via API and must be adjusted in the automation builder UI.
- **Mailbox / outbound email integration** requires UI credential authorization and often client sign-off before enabling.
- **Formula column bodies** may need to be entered/edited in the UI.
- **Mirror columns** require a pre-existing Connect Boards column and are sometimes completed manually.
- **Dashboard widgets** are configured in the UI; API creation is limited.
- **Filtered views** (e.g. a "Today" table) are commonly added manually in the UI.
- **Specific person assignment** in automations/People columns may need manual selection.
- **Template leftovers** — default columns/groups from a template that need hiding, renaming, or deleting.
- **Sharing / permissions** changes (making a board private, inviting guests) may require account-admin action.

## Owner / Theme Header Guide

Use short, human-readable headers. Only emit headers that have items:
- `### Fix (validation defects)` — flagged defects needing correction.
- `### Consultant (in monday)` — manual build/config steps the builder must finish.
- `### Needs client decision` — approvals, sign-offs, choices the client owes.
- `### Cleanup / polish` — cosmetic/leftover-template tasks.
- `### Blocked / platform limits` — items that can't proceed due to a documented monday.com limitation; note the accepted exception.
- `### Communicate / document` — accepted exceptions or trade-offs to be relayed or written up.

## Reminders

- Every item is a checkbox. No bullets, numbers, or prose.
- One imperative action per checkbox.
- Tag the source in parentheses whenever it aids traceability.
- End with the checklist — nothing after it.
