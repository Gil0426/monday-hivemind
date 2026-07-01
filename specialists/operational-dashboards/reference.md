# Operational Dashboards — Reference

## Widgets used (operational toolkit)

| Widget | Operational use | Notes |
|---|---|---|
| **Table** | The workhorse — filtered lists of "my open items", overdue tasks, unpaid bookings. | Supports filters, sort, and column selection. Can source multiple boards. Primary action surface. |
| **Numbers** | At-a-glance counts: "# follow-ups due today", "# unpaid bookings". | Count of items, or sum/avg of a numeric column. Apply filters to scope the count. Big single value — perfect for top-left. |
| **Battery** | Status distribution at a glance (e.g. bookings by stage). | Compact; shows proportions of a Status column. Use sparingly — operationally useful only when distribution drives action. |
| **Chart** | Simple bar/column where a quick visual beats a list. | Keep minimal. Avoid line/trend charts (that's analytical). |
| **Countdown / Time-based** | Optional deadline emphasis. | Only if a specific real deadline exists. |

## Widget filter types

| Filter kind | Operational examples |
|---|---|
| **Date filters** | `Today`, `This week`, `Overdue` (past due), `Done` states, or "in the next N days" via date range conditions. Applied to Date/Timeline columns. |
| **Status filters** | `Deposit Status = Unpaid`, `Stage = <value>`, `Payment = Overdue`. Applied to Status/Dropdown columns. |
| **People filters** | `Person = assigned to me`, or a specific on-duty rep. Applied to People column. `assigned to me` makes one dashboard personal per viewer. |
| **Combined** | Multiple conditions AND/OR — e.g. `Deposit Status = Unpaid` AND `Stay Start within next 7 days`. |

## Column types (that dashboards filter/count on)

| Column | Type ID | Operational role |
|---|---|---|
| Status | `status` | Stage, Deposit Status, Payment Status — primary exception/status filters. |
| Dropdown | `dropdown` | Multi-value categories (e.g. tags, service type). |
| Date | `date` | Due dates, follow-up dates, stay start, expiry dates — powers Today/Overdue/next-N-days filters. |
| Timeline | `timeline` | Date ranges (e.g. stay start–end). |
| People | `people` | Assigned rep / on-duty person for people filters. |
| Numbers | `numbers` | Amounts (deposit due, balance) — summed in Numbers widget. |
| Text | `text` | Names, notes (display in tables). |
| Connect boards | `board_relation` | Links Bookings↔Dogs↔Leads (relationship, not a dashboard filter substitute). |
| Mirror | `mirror` | Surfaces a linked board's value in a table column. Note: mirror columns have **filtering limitations** in some widgets. |
| Formula | `formula` | Derived values. Note: formula columns are **not filterable/aggregatable** in most dashboard widgets — store the value in a real column if you need to filter on it. |

## Example board structures (doggy-daycare CRM)

### Leads board
| Column | Type |
|---|---|
| Lead Name | `text` (item name) |
| Stage | `status` |
| Follow-up Date | `date` |
| Owner | `people` |
| Dog(s) | `board_relation` |

### Bookings board
| Column | Type |
|---|---|
| Booking | `text` (item name) |
| Stage | `status` |
| Deposit Status | `status` |
| Deposit Amount | `numbers` |
| Stay | `timeline` |
| Stay Start | `date` |
| Assigned Rep | `people` |
| Dog | `board_relation` |

### Dogs board
| Column | Type |
|---|---|
| Dog Name | `text` (item name) |
| Vaccination Expiry | `date` |
| Vaccination Status | `status` |
| Owner (client) | `text` |
| Bookings | `board_relation` |

## Status label JSON (examples)

**Stage (Leads):**
```json
{
  "labels": {
    "0": "New",
    "1": "Contacted",
    "2": "Trial Booked",
    "3": "Won",
    "4": "Lost"
  }
}
```

**Deposit Status (Bookings):**
```json
{
  "labels": {
    "0": "Unpaid",
    "1": "Partial",
    "2": "Paid"
  }
}
```

**Vaccination Status (Dogs):**
```json
{
  "labels": {
    "0": "Valid",
    "1": "Expiring Soon",
    "2": "Expired"
  }
}
```

## Example dashboard layout (front-desk "Today")

```
┌────────────┬────────────┬────────────┬────────────┐
│ Numbers    │ Numbers    │ Numbers    │ Battery     │
│ Follow-ups │ Unpaid     │ Vax        │ Leads by    │
│ due today  │ bookings   │ expiring   │ stage       │
│  (count)   │  (count)   │ ≤14d(count)│             │
├────────────┴────────────┴────────────┴────────────┤
│ Table: Follow-ups due today (Leads)                │
│  filter: Follow-up Date = Today, Owner = me        │
├────────────────────────────────────────────────────┤
│ Table: Unpaid deposits, stay starts ≤7 days        │
│  (Bookings) filter: Deposit Status = Unpaid         │
│  AND Stay Start within next 7 days                  │
├────────────────────────────────────────────────────┤
│ Table: Vaccinations expiring ≤14 days (Dogs)        │
│  filter: Vaccination Expiry within next 14 days     │
└────────────────────────────────────────────────────┘
```
Counters top-left (highest attention), action tables below, one Battery only because stage distribution helps triage. No trend charts.

## Limitations (real monday.com constraints)

- **Board-count limit per dashboard.** Depends on plan (commonly up to 5 boards on lower tiers; higher on Pro/Enterprise). Confirm before designing wide cross-board dashboards.
- **Formula columns can't be filtered/aggregated** in most dashboard widgets. If you need to filter/count on a derived value, compute it into a real Status/Numbers column via automation or manual entry.
- **Mirror column limitations.** Mirror columns may not be fully filterable/summable in all widgets. Prefer native columns on the source board for filters and counts.
- **"Next N days" is expressed via date-range conditions**, not always a single named preset. Named presets like `Today`, `This week`, `Overdue`, `Past dates` exist; arbitrary ranges use date condition filters.
- **`assigned to me` is viewer-relative** — great for personal front-desk views, but means each user sees their own items. For a shared team board view, filter by a specific person or leave people unfiltered.
- **Dashboards are read-only visualizations.** You cannot create/edit item data from most widgets (Table widget allows limited interaction depending on settings, but treat dashboards as read/scan surfaces). Data entry happens on boards.
- **No trend/forecast native operational widget.** Period-over-period, win-rate, conversion, and forecasting are analytical — out of scope here. Route to the **analytics-dashboards** specialist.
- **Counts reflect current filtered data**, not historical snapshots. A Numbers counter shows "right now," which is exactly what operational views want — but it is not a trend.
