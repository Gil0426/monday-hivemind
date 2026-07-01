# Validation Specialist — Reference

## How to read live state

- **Board list / board info** — confirms each named board exists; detects unintended duplicates (e.g. two "Leads" boards, or a copy of a template board left behind).
- **Column metadata** — returns each column's `id`, `title`, and `type`. Use `type` to confirm the field is the correct kind (native number vs mirror vs formula, etc.).
- **Column settings** — for `status`/`dropdown`, returns the label set and index order; for `board_relation`, returns the connected board(s) and whether the link is single/multiple; for `mirror`, returns the source connect column and mirrored column.
- **Automation / recipe listing** — returns configured automations so you can verify trigger, conditions, and actions against the blueprint. Compare intent, not just count.
- **Views / widgets** — confirm required saved views and dashboard widgets exist per the deliverables list.
- **Items** — confirm required sample data rows exist.

Trust **this** state, not the build report.

## Column Types Table (type identifiers)

| Column | API `type` | Common use | Validation notes |
|---|---|---|---|
| Text | `text` | free text, notes | plain string; no formatting |
| Long Text | `long_text` | descriptions | distinct from `text` |
| Numbers | `numbers` | deposit, price, qty | **native value** — can drive automations & formulas. If spec says a number must drive logic, it MUST be this, not `mirror`/`formula`. |
| Status | `status` | pipeline stage, state | label set + **index order** matter; verify exact list |
| Dropdown | `dropdown` | multi-select tags | multiple labels selectable; different from `status` |
| Date | `date` | booking date, due | supports time; used by date-based automations |
| Timeline | `timeline` | start–end range | two dates; not the same as `date` |
| People | `people` | assignee, owner | internal users/teams only |
| Email | `email` | contact email | **cannot email external owners via automation without an integration** |
| Phone | `phone` | contact phone | |
| Link | `link` | URLs | |
| Connect Boards (board_relation) | `board_relation` | Lead→Owner, Owner↔Dogs | verify **connected board** and **direction**; single vs multiple |
| Mirror | `mirror` | show linked board's value | **read-only reflection** — CANNOT drive automations or be edited. FAIL if spec needs a native value. |
| Formula | `formula` | computed value | **read-only, not stored** — cannot trigger automations or be mirrored reliably |
| Files | `file` | attachments | |
| Checkbox | `checkbox` | boolean flag | |
| Rating | `rating` | score | |
| Hour | `hour` | time of day | |
| Tags | `tags` | shared tags | cross-board tags |
| Dependency | `dependency` | task dependencies | |
| Item ID | `item_id` | system id | auto |
| Auto Number | `auto_number` | sequence | auto |
| Creation Log | `creation_log` | created by/at | auto |
| Last Updated | `last_updated` | updated by/at | auto |
| Country / Location | `country` / `location` | geo | |
| Color Picker | `color_picker` | color | |
| Vote | `vote` | votes | |
| World Clock | `world_clock` | timezone | |

### Critical type-substitution defects to catch
- **Mirror used where native Numbers required** → FAIL. A mirror is read-only and cannot drive `numbers`-based automations/conditions.
- **Formula used where a stored/triggering value required** → FAIL. Formulas don't persist and can't trigger automations.
- **Dropdown used where Status required (or vice versa)** → PARTIAL/FAIL depending on whether automations/labels depend on it.
- **Text used where Numbers/Date required** → FAIL; breaks math and date automations.
- **Date used where Timeline required** (or reverse) → FAIL; ranges vs single points differ.

## Board Structure Validation

For each board in the doc, verify:
1. **Existence** — board present, correct name.
2. **No unintended duplicates** — especially leftover copies of template boards.
3. **Column set** — every documented field present, correct `type`, correct settings/labels.
4. **Connections** — `board_relation` columns point to the correct board, in the documented direction, single vs multiple as specified, with **reflection/mirror columns present** where the doc requires the linked value to be visible.
5. **Views/widgets** — required saved views exist.
6. **Sample data** — required rows exist.

### Connection direction & reflection
A `board_relation` is directional in intent even when technically two-way. Validate the **documented direction** and the presence of the **reflection**:

- **Lead → Owner**: Leads board has a `board_relation` to Owners. Verify it targets Owners, single-select if the doc says one owner per lead.
- **Owner ↔ Dogs**: bidirectional link. Verify the connect column on Owners targets Dogs AND the reflection is visible on Dogs (either the auto two-way connect column or a `mirror`).
- **Booking → Owner / Dogs**: Bookings board has connect columns to both Owners and Dogs. Verify **two separate** relations, each to the correct board, plus any required mirror of owner/dog fields onto Booking.

Missing reflection where the doc requires the linked value visible = **PARTIAL** (link exists, reflection absent).
Wrong target board or reversed single/multiple = **FAIL**.

## Status Label JSON (verify labels AND order)

`status` and `dropdown` columns carry an indexed label set. The documented stage list must match **exactly, in the documented order**. Example expected pipeline:

```json
{
  "labels": {
    "0": "New Lead",
    "1": "Contacted",
    "2": "Qualified",
    "3": "Proposal Sent",
    "4": "Won",
    "5": "Lost"
  }
}
```
