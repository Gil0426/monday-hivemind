# monday.com Reference — Board Building for Actionable Information / SOW

## Relevant Column Types (with Type IDs)

monday.com columns are identified by an internal `type` string used in the API. Common, real column types relevant to this domain:

| Column Type | API `type` ID | Use in SOW/Extracted-Info Boards |
|-------------|---------------|----------------------------------|
| Status | `status` (a.k.a. `color`) | Lifecycle/stage of a deliverable; drives most automations |
| Text | `text` | Short free text (notes, reference codes) |
| Long Text | `long_text` | Acceptance criteria, scope descriptions |
| Numbers | `numbers` | Costs, hours, quantities |
| People | `people` | Owner/assignee; triggers assignment automations |
| Date | `date` | Due dates, milestone dates; drives date-based automations |
| Timeline | `timeline` | Start/end date ranges for phases |
| Dropdown | `dropdown` | Multi-select tags (e.g., multiple categories) |
| Status (Priority) | `status` | Priority levels (configured as a status column) |
| Checkbox | `checkbox` | Simple done/not-done flags |
| Link | `link` | URLs to source docs, SOW files |
| Files | `file` | Attached SOW PDFs, contracts |
| Dependency | `dependency` | Links predecessor/successor items |
| Connect Boards | `board_relation` | Relate items across boards |
| Mirror | `mirror` | Display data from connected boards (read-only) |
| Formula | `formula` | Calculations within the same board |
| Email | `email` | Contact emails |
| Phone | `phone` | Contact phone numbers |
| Hour | `hour` | Time-of-day values |
| Rating | `rating` | Quality/satisfaction scoring |

> Note: The Status column's historical/internal API type is often `color`. Confirm against the current monday.com API version before building programmatically.

## Typical Board Structure for SOW / Extracted Info

### Groups (phases or categories)

| Group | Purpose |
|-------|---------|
| Discovery / Requirements | Items extracted from SOW scope definition |
| Deliverables | Concrete outputs the SOW commits to |
| Milestones | Key dated checkpoints |
| Dependencies / Risks | Items flagged as blockers or assumptions |
| Closed / Accepted | Completed and signed-off work |

### Columns (recommended set)

| Column Name | Type ID | Notes |
|-------------|---------|-------|
| Status | `status` | Workflow stage |
| Owner | `people` | Responsible party |
| Due Date | `date` | Deadline (automation trigger) |
| Timeline | `timeline` | Phase span |
| Priority | `status` | High/Medium/Low |
| Category | `dropdown` | Multi-tag classification |
| Scope / Acceptance | `long_text` | Detailed criteria from SOW |
| Cost | `numbers` | Budget value |
| Est. Hours | `numbers` | Effort estimate |
| Source Doc | `link` or `file` | Traceability to original SOW |
| Dependencies | `dependency` | Predecessor/successor |

## Status Label Configurations

Status labels carry an **index**, a **label text**, and a **color**. Suggested configurations:

**Workflow Status**
| Index | Label | Color (name) |
|-------|-------|--------------|
| 0 | Not Started | Grey (`#c4c4c4`) |
| 1 | In Progress | Orange |
| 2 | Blocked | Red |
| 3 | In Review | Yellow |
| 4 | Done | Green |

**Priority Status**
| Index | Label | Color |
|-------|-------|-------|
| 0 | Low | Light blue |
| 1 | Medium | Yellow |
| 2 | High | Red |
| 3 | Critical | Dark red |

> Status columns are **single-select**. If an item needs multiple simultaneous tags, use a Dropdown column.

## Documented Limitations

- **Status = single select.** One label per item; use Dropdown for multi-value.
- **Subitems are one level deep.** No sub-subitems.
- **Mirror columns are read-only** and reflect connected-board values; they cannot be edited or, in some cases, used as automation triggers.
- **Formula columns compute within the same board only**, are recalculated on view, and are not stored as static values.
- **Automation and integration action counts are plan-limited.** Free/lower tiers cap monthly actions.
- **Item/column/board limits** apply per plan (e.g., automation actions, number of boards, file storage). Always verify current quotas for the customer's plan.
- **Dependencies do not auto-reschedule by critical path** beyond explicit dependency-shift automations you enable.
- **No column-level "required" enforcement.** Data completeness must be encouraged via process or automation reminders, not hard validation.
- **People column assignments** can trigger notifications, but you cannot enforce a single mandatory owner at the schema level.

> Ground all builds in these documented capabilities. Do not promise critical-path engines, multi-select status, cross-board formulas, or required-field validation — monday.com does not provide them.
