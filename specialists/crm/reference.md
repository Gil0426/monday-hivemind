# CRM Board Reference — monday.com

Source: https://support.monday.com/hc/en-us/categories/360000578891-CRM
Use this as your primary grounding. Search official docs for anything not covered here.

---

## CRM Architecture Options

### Option A — 3-Board CRM (mature setup)
1. **Deals / Pipeline** — one item per opportunity (primary board)
2. **Contacts** — one item per person; linked to Deals via `board_relation`
3. **Companies / Accounts** — one item per organization; linked to Contacts and Deals

### Option B — 1-Board CRM (small teams, fast start)
Single Deals board with `text` columns for contact name and company name.
Migrate to Option A when the team outgrows it.

---

## Deals / Pipeline Board

### Groups-as-Stages vs. Status-as-Stage

| Approach | When to use |
|---|---|
| **Groups = pipeline stages** | When you want bulk-move items between stages, color-coded rows by stage, and stage-level filtering. Best for visual pipeline management. |
| **Status column = stage** | When you want all deals in one scrollable list with filtering/grouping by status. Best for reporting and cross-stage search. |

Both approaches are valid. Groups-as-stages is more visual; status-as-stage is more flexible.

### Recommended Groups (groups-as-stages pattern)
- Prospecting
- Qualification
- Proposal Sent
- Negotiation
- Closed Won
- Closed Lost

### Essential Columns — Deals Board

| Column Title | Type ID | Settings / Notes |
|---|---|---|
| Deal Name | *(Name col)* | Automatic — always first, always text |
| Stage | `status` | Labels: `0`=New, `1`=Prospecting, `2`=Qualified, `3`=Proposal, `4`=Negotiation, `5`=Won, `6`=Lost |
| Deal Value | `numbers` | Store in a single currency. Footer: sum for total pipeline value. |
| Close Date | `date` | Expected close date. Use Calendar view on this column. |
| Owner | `people` | Sales rep assigned. Workspace users only. |
| Contact Name | `text` or `board_relation` | Text = simple; board_relation = links to Contacts board |
| Company | `text` or `board_relation` | Text = simple; board_relation = links to Companies board |
| Lead Source | `dropdown` | Options: Inbound, Outbound, Referral, Partner, Event, Cold Call, Other |
| Priority | `status` | Labels: `0`=None, `1`=Hot, `2`=Warm, `3`=Cold |
| Probability | `numbers` | 0–100 percentage. Can feed a formula for weighted pipeline value. |
| Weighted Value | `formula` | `{Deal Value} * {Probability} / 100` (if formula syntax supported) |
| Next Action | `text` | Short description of next step |
| Next Action Date | `date` | Follow-up date |
| Notes | `long_text` | Free-form deal notes |
| Last Activity | `last_updated` | Auto-updates on any change. Read-only. |
| Deal Link | `link` | Link to proposal doc, deck, or external CRM record |

### Status Label Configuration — Stage column
```json
{"labels": {"0": "New", "1": "Prospecting", "2": "Qualified", "3": "Proposal Sent", "4": "Negotiation", "5": "Closed Won", "6": "Closed Lost"}}
```

---

## Contacts Board

| Column Title | Type ID | Notes |
|---|---|---|
| Full Name | *(Name col)* | Automatic |
| Title / Role | `text` | Job title |
| Company | `text` or `board_relation` | Links to Companies board |
| Email | `email` | Display only |
| Phone | `phone` | Display only |
| LinkedIn | `link` | Profile URL |
| Owner | `people` | Assigned rep |
| Contact Status | `status` | Labels: Prospect, Active, Customer, Churned, Unqualified |
| Tags | `tags` | Freeform labels (industry, persona, source) |
| Notes | `long_text` | Relationship notes |
| Linked Deals | `board_relation` | Links to Deals board |
| Last Contacted | `date` | Manual date of last outreach |

---

## Companies / Accounts Board

| Column Title | Type ID | Notes |
|---|---|---|
| Company Name | *(Name col)* | Automatic |
| Industry | `dropdown` | Options: SaaS, Fintech, Healthcare, Retail, Manufacturing, Services, Other |
| Company Size | `dropdown` | Options: 1–10, 11–50, 51–200, 201–1000, 1000+ |
| Website | `link` | Company website URL |
| HQ Location | `location` | Headquarters address |
| Annual Revenue | `numbers` | Estimated ARR or revenue |
| Account Owner | `people` | Assigned account manager |
| Relationship Status | `status` | Labels: Prospect, Active Customer, Partner, At Risk, Churned |
| Linked Contacts | `board_relation` | Links to Contacts board |
| Linked Deals | `board_relation` | Links to Deals board |
| Notes | `long_text` | Account notes |

---

## Known monday.com CRM Limitations

- **No native email client**: `email` and `phone` columns are display/link only. Use monday.com's
  Gmail/Outlook integration or third-party tools for actual outreach.
- **No deduplication**: monday.com will create duplicate contacts and companies without warning.
- **No lead scoring across boards**: formula columns are board-scoped; cannot read from linked boards.
- **No account hierarchy**: parent/child company relationships require a workaround
  (a `board_relation` to the same board, or a hierarchy column).
- **No native currency conversion**: all monetary values must be stored in one currency.
- **people column = workspace users only**: cannot assign external contacts to a People column.
- **board_relation grid view**: shows only item count; click to see linked items in detail.
- **Automations are separate**: Do not promise automation behavior (e.g., "when deal is Won,
  notify owner") — automations are configured by the user in monday.com's Automations Center,
  not via board design.

---

## Recommended CRM Views

| View | Column Required | Purpose |
|---|---|---|
| Kanban | `status` (Stage) | Visual pipeline by stage |
| Calendar | `date` (Close Date) | Upcoming close dates |
| Chart — Bar | `status` (Stage) | Deal count by stage |
| Chart — Pie | `dropdown` (Lead Source) | Deals by source |
| Dashboard — Numbers widget | `numbers` (Deal Value) | Total pipeline value |
| Dashboard — Chart widget | `people` (Owner) | Pipeline by rep |
