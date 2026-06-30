# monday.com Core Reference

Source: https://support.monday.com / https://developer.monday.com
Use this as your primary grounding. For anything not covered here, search the official docs.

---

## Board Types

| Kind | Description |
|---|---|
| `public` | Visible to all workspace members |
| `private` | Visible only to invited members |
| `share` | Accessible via a shareable link (for external stakeholders) |

---

## Column Types (official monday.com type IDs)

### Status & Progress
| Type ID | Label | Notes |
|---|---|---|
| `status` | Status | Color-coded labels. Customizable per board. Default: Not Started / In Progress / Done / Stuck. Max ~20 labels. Index 0 = empty/gray state. |
| `checkbox` | Checkbox | Boolean yes/no. |
| `rating` | Rating | 1–5 stars. |
| `progress` | Progress | 0–100% bar. Manual input or auto-calculated from subitems (requires automation). |

### Date & Time
| Type ID | Label | Notes |
|---|---|---|
| `date` | Date | Single date with optional time. Supports Calendar view. |
| `timeline` | Timeline | Start + end date range. **Required for Gantt/Timeline view.** A `date` column alone does NOT appear on Gantt. |
| `week` | Week | Calendar week picker. |
| `time_tracking` | Time Tracking | Start/stop timer. Requires user to be logged in and manually trigger. Does not auto-track. |
| `world_clock` | World Clock | Shows current time in a named timezone. Display only. |

### People & Teams
| Type ID | Label | Notes |
|---|---|---|
| `people` | Person | Assigns monday.com workspace users. Supports multiple assignees. External contacts cannot be assigned. |
| `team` | Team | Assigns a monday.com team object. |

### Text & Numbers
| Type ID | Label | Notes |
|---|---|---|
| `text` | Text | Short single-line text. |
| `long_text` | Long Text | Multi-line rich text. |
| `numbers` | Numbers | Numeric value. Column footer supports sum, average, min, max. |
| `formula` | Formula | Calculated read-only field. Uses monday.com formula language (not JS/Python). Can reference columns on the same board only. |
| `auto_number` | Auto Number | Auto-incrementing integer. Read-only. Resets if rows are reordered. |
| `item_id` | Item ID | Shows the item's unique monday.com ID. Read-only. |

### Contact & Web
| Type ID | Label | Notes |
|---|---|---|
| `email` | Email | Email address with mailto link. Display only — monday.com is not an email client. |
| `phone` | Phone | Phone number with click-to-call. Display only. |
| `link` | Link | URL with optional display label. |

### Categorization
| Type ID | Label | Notes |
|---|---|---|
| `dropdown` | Dropdown | Single or multi-select from a fixed list. Configure `labels` in settings. |
| `tags` | Tags | Freeform multi-tag. Tags are shared across the whole board. |
| `country` | Country | Country picker. |
| `color_picker` | Color Picker | Hex color selector. |
| `location` | Location | Address with map preview. |

### Relationships
| Type ID | Label | Notes |
|---|---|---|
| `board_relation` | Connect Boards | Links items to items on another board (or same board). Required for cross-board linking. |
| `dependency` | Dependency | Links items within the **same board** for sequencing. Does NOT work cross-board. |

### Files
| Type ID | Label | Notes |
|---|---|---|
| `file` | File | File attachments. Supports local upload, Google Drive, Dropbox, Box. |

### Audit / Metadata (read-only)
| Type ID | Label | Notes |
|---|---|---|
| `creation_log` | Creation Log | Who created the item and when. Read-only. |
| `last_updated` | Last Updated | Who last modified the item and when. Read-only. |

---

## Status Column Settings Format

```json
{"labels": {"0": "Not Started", "1": "In Progress", "2": "Done", "3": "Stuck"}}
```

Index `0` is always the default empty/gray state. Indexes 1+ are colored. You can define up to ~20 labels.
Use descriptive, domain-specific labels rather than generic ones where possible.

---

## Dropdown Column Settings Format

```json
{"settings": {"labels": [{"name": "Option A"}, {"name": "Option B"}, {"name": "Option C"}]}}
```

---

## Board Structure Conventions

- **Groups**: 3–7 groups per board is typical. A group is a horizontal section with its own color label.
  Groups can represent pipeline stages, phases, categories, or teams.
- **The Name column**: Always the first column. Cannot be removed, reordered, or given a type.
  It is always a text title field.
- **Items**: 5–20 items per group for readable boards. Items are the rows.
- **Column count**: monday.com supports many columns but 8–12 is practical for grid readability.

---

## What monday.com Does NOT Support at Board Level

- Required/mandatory fields — no column can be enforced as required.
- Formulas that read from other boards — formula columns are board-scoped.
- Field-level permissions — column visibility is all-or-nothing per board.
- Automatic deduplication of items.
- Native currency conversion (pick one currency and stick to it).
- Subitems sharing column definitions with the parent board — subitem columns are independent.
- Cross-board dependency tracking — use `board_relation` and manual coordination instead.
