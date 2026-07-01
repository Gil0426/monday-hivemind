# Documentation Reference

This reference helps you accurately describe monday.com objects in your documentation. Use the correct type names and be precise about behavior.

## Column Types (type IDs)

When reading a board with `get_board_info`, columns report a `type`. Reference table for accurate documentation (include IDs in **runbooks only**, not end-user guides):

| Column Type | Type ID | What to tell the reader |
|---|---|---|
| Status | `status` | Colored labels; one selection. Drives most automations. |
| Dropdown | `dropdown` | Multiple tags/labels selectable. |
| Text | `text` | Short single-line text. |
| Long Text | `long_text` | Multi-line notes. |
| Numbers | `numbers` | Numeric value, optional unit. |
| People | `people` | Assign persons/teams. |
| Date | `date` | Date, optional time. |
| Timeline | `timeline` | Start–end date range. |
| Email | `email` | Email address (clickable). |
| Phone | `phone` | Phone number. |
| Link | `link` | URL with display text. |
| Checkbox | `checkbox` | On/off toggle. |
| Rating | `rating` | Star rating. |
| Tags | `tags` | Shared tags across boards. |
| Timeline/Hour | `hour` | Time of day. |
| Week | `week` | Week range. |
| Files | `file` | Uploaded files/images. |
| Dependency | `dependency` | Links items whose dates depend on each other. |
| Connect Boards | `board_relation` | Links items across boards. |
| Mirror | `mirror` | **Read-only** reflection of a connected board's column. Edit at source. |
| Formula | `formula` | Calculated value; **read-only**, not stored, not automation-triggerable in most cases. |
| Item ID | `item_id` | System unique ID. |
| Creation Log | `creation_log` | Who/when created. |
| Last Updated | `last_updated` | Who/when last changed. |
| Time Tracking | `time_tracking` | Accumulated tracked time. |
| Country | `country` | Country selector. |
| Location | `location` | Address with map. |
| Vote | `vote` | Per-person votes. |
| Color Picker / Progress | `color`, `progress` | Progress = weighted status/checkbox rollup, read-only. |

**Documentation notes on behavior:**
- **Mirror** and **Formula** columns are read-only for the user — always tell users to edit the *source*.
- **Formula** columns generally cannot trigger automations — don't document automation behavior tied to them without verifying.
- **Connect Boards** (`board_relation`) is what makes mirrors and cross-board automations possible; if a mirror shows blank, the connect column is usually the cause.

## Board Structure Concepts

Describe these accurately:

- **Board** — a workspace of items. Has a name (use it exactly).
- **Groups** — colored sections within a board (often pipeline stages or categories). Use exact group titles.
- **Items** — rows. Name them by what they represent to the reader (e.g., "each lead is one item").
- **Subitems** — nested rows under an item; have their own columns.
- **Views** — saved filters/layouts (Table, Kanban, Calendar, Chart, Form, etc.). Reference views by their exact saved name.
- **Dashboards** — cross-board widgets; separate object from boards.
- **Workspace** — container for boards/docs. monday workdocs (`create_doc`) live here, next to the boards.

## Status Label JSON

Status and Dropdown labels have index → label → color mappings. Read them from `get_board_info` and document the **exact labels** the user will see. Example structure:

```json
{
  "labels": {
    "0": "New Lead",
    "1": "Contacted",
    "2": "Qualified",
    "3": "Won",
    "4": "Lost"
  },
  "labels_colors": {
    "0": { "color": "#c4c4c4", "border": "#b0b0b0" },
    "3": { "color": "#00c875", "border": "#00b461" },
    "4": { "color": "#e2445c", "border": "#ce3048" }
  }
}
```

**Documentation rule:** quote the label text exactly as it appears (e.g., "set the status to **Qualified**", not "mark it qualified"). Colors help you describe them in guides ("the green **Won** label").

## Automations — how to document them

Read with `list_automations`. For each automation, capture and document:
- **Trigger** (e.g., "When status changes to *Lost*")
- **Condition** (if any)
- **Action** (e.g., "notify item owner", "create item in board X", "send email")
- **Real-world effect and limitation** — critically: does it **block** or merely **notify**? Does it depend on an integration?

Common patterns to describe precisely:
| Behavior | How to phrase it honestly |
|---|---|
| Notification automation | "**Notifies** — it does not prevent the action." |
| Status-change → create item | "Creates a linked item automatically; may take a few seconds." |
| Email automation | "**Requires the mailbox/email integration to be connected.** If disconnected, no email is sent and there is no error to the user." |
| Recurring automation | State the schedule exactly (e.g., "every Monday 8:00 AM"). |
| Cross-board automation | Depends on a **Connect Boards** column being populated. |

## Agents — how to document them

Read with `manage_agent`. Document:
- Agent name and purpose.
- What triggers it and what it acts on (which board/columns).
- Its scope and permissions.
- **Limitations**: agents act on available context; document what it will and won't do.

## Limitations Section (include in every relevant doc)

Standard honest limitations to check for and state when true:

1. **Notify-not-block automations** — many rules notify rather than enforce; users can still proceed.
2. **Integration dependencies** — email, calendar, Slack, etc. require an active integration; silent failure if disconnected.
3. **Mirror/Formula read-only** — cannot be edited in place; formula values may not trigger automations.
4. **Automation timing** — automations are near-real-time, not instant; brief delays are normal.
5. **Permissions** — some columns/boards may be view-only for certain user roles; a step may fail for lower-permission users.
6. **Recurring automations** run on schedule, not on demand.
7. **Deletion/undo** — deleted items go to Recycle Bin (recoverable ~30 days); note if a workflow relies on this.
8. **Subitem columns are separate** from parent columns; automations must target the right level.

Always cross-check each stated limitation against the live build. If you cannot verify, mark `[VERIFY: ...]`.

## Document Templates — required elements

Every deliverable includes a header block and change log:

```markdown
# [Document Title]
**Audience:** [who this is for]
**System:** [board/workspace name]
**Version:** 1.0  |  **Date:** YYYY-MM-DD  |  **Author:** Documentation Specialist

---
[body]
---

## Change Log
| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0 | YYYY-MM-DD | Documentation Specialist | Initial release. |
```

### One-pager structure (keep to one page)
1. Title + version line.
2. "Your top tasks
