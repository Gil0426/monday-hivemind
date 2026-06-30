# Project Management Board Reference — monday.com

Source: https://support.monday.com/hc/en-us/categories/360001525585-Project-Management
Use this as primary grounding. Search official docs for anything not covered here.

---

## Board Architecture Options

| Pattern | When to use |
|---|---|
| **Single task board** | One project, all tasks in one place, groups = phases |
| **Sprint / agile board** | Iterative dev work; groups = sprints or backlog |
| **Portfolio board** | Many projects; one item per project; links to project boards |
| **Resource board** | People-centric; groups = team members or departments |

---

## Single Project Task Board

### Recommended Groups
- Backlog
- To Do
- In Progress
- In Review / QA
- Done
- Blocked / On Hold

### Essential Columns

| Column Title | Type ID | Notes |
|---|---|---|
| Task Name | *(Name col)* | Automatic — always first |
| Status | `status` | See Status Labels below |
| Owner | `people` | Assigned team member(s). Supports multiple. |
| Due Date | `date` | Task deadline. Powers Calendar view. |
| Timeline | `timeline` | Start → end date. **Required for Gantt/Timeline view.** |
| Priority | `status` | Labels: Critical / High / Medium / Low |
| Effort (pts) | `numbers` | Story points or hours estimate. Footer: sum. |
| % Complete | `numbers` | Manual 0–100 progress. |
| Dependencies | `dependency` | Links blocking tasks on the **same board** only. |
| Tags | `tags` | Feature area, component, or sprint label. |
| Notes | `long_text` | Task description or acceptance criteria. |
| Attachments | `file` | Linked specs, mockups, test plans. |
| Related Link | `link` | PR, Jira ticket, Figma frame, or doc URL. |
| Time Tracked | `time_tracking` | Manual timer — requires user to start/stop. |
| Created By | `creation_log` | Who created the task. Read-only. |
| Last Updated | `last_updated` | Who last touched the task. Read-only. |

### Status Labels — Task Status column
```json
{"labels": {"0": "Not Started", "1": "In Progress", "2": "In Review", "3": "Done", "4": "Blocked"}}
```

### Status Labels — Priority column
```json
{"labels": {"0": "None", "1": "Critical", "2": "High", "3": "Medium", "4": "Low"}}
```

---

## Sprint / Agile Board

Groups = sprints (Sprint 1, Sprint 2, Backlog, Done)

| Column Title | Type ID | Notes |
|---|---|---|
| Story / Task Name | *(Name col)* | Automatic |
| Story Points | `numbers` | Effort estimate. Footer: sum for sprint total. |
| Status | `status` | Backlog / To Do / In Progress / In Review / Done |
| Type | `status` | Feature / Bug / Chore / Spike |
| Owner | `people` | Assigned developer |
| Priority | `status` | P0 (Critical) / P1 (High) / P2 (Medium) / P3 (Low) |
| Epic | `dropdown` | Epic or feature area this story belongs to |
| Due Date | `date` | Target completion within sprint |
| PR / Branch | `link` | GitHub / GitLab pull request or branch URL |
| Blocked By | `dependency` | Blocking stories on the same board |
| Notes | `long_text` | Acceptance criteria or context |

---

## Portfolio Board (Multi-Project Tracker)

Groups: Active Projects / Planning / On Hold / Completed / Cancelled

| Column Title | Type ID | Notes |
|---|---|---|
| Project Name | *(Name col)* | Automatic |
| Status | `status` | Planning / Active / On Hold / Complete / Cancelled |
| Health | `status` | On Track / At Risk / Off Track |
| Phase | `status` | Initiation / Planning / Execution / Closure |
| Project Owner | `people` | Project lead |
| Start Date | `date` | Planned start |
| End Date | `date` | Planned completion |
| Timeline | `timeline` | Start → end for Gantt rollup view |
| Budget | `numbers` | Allocated budget |
| Spent | `numbers` | Current spend |
| Team | `people` | All team members |
| Tags | `tags` | Department, client, product area |
| Project Board | `board_relation` | Links to the individual project's task board |
| Notes | `long_text` | Executive summary or status update |

---

## Resource / Capacity Planning Pattern

To plan workload across team members:
- Use a `people` column for assignment
- Use a `numbers` column for allocation (hours or %)
- Use the **Workload widget** on a Dashboard — it reads `people` + `numbers` (effort) columns
  across boards. This requires connecting the boards to a Dashboard.

A dedicated Resource board can use groups = team members, items = their assigned projects.

---

## Key monday.com Project Management Limitations

- **dependency column is same-board only**: Cross-board task dependencies require `board_relation`
  + manual process. There is no native cross-board critical path.
- **timeline ≠ date**: Only `timeline` columns appear in the Gantt/Timeline view.
  A `date` column appears only in Calendar view. Use both if you need both views.
- **Subitem columns are independent**: Subitems have their own column set separate from the
  parent board. You cannot roll up subitem field values into the parent's columns without a formula
  or automation.
- **Progress % is manual by default**: The `progress` column is manually set (0–100). Auto-progress
  from subtask completion requires a monday.com automation rule, not board design.
- **time_tracking requires manual start/stop**: It does not integrate with calendars or auto-track
  time spent. The logged-in user must click Start/Stop.
- **formula is board-scoped and read-only**: Cannot reference columns from other boards. Cannot
  run arbitrary code. Uses monday.com's own formula language.
- **Automations are separate**: Status-change notifications, deadline alerts, and assignment
  triggers are configured in Automations Center — not part of board design.

---

## Recommended Views for Project Boards

| View | Requires | Purpose |
|---|---|---|
| Timeline / Gantt | `timeline` column | Visual project timeline with dependencies |
| Kanban | `status` column | Card-based task flow |
| Calendar | `date` column | Deadline calendar |
| Workload | `people` + `numbers` | Capacity planning per person |
| Chart — Bar | `status` | Tasks by status or owner |
| Chart — Pie | `people` | Work distribution across team |
