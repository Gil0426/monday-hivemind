# Analytics & Dashboards Reference

## Widgets Used for Analytics

| Widget | Best for | Key configuration |
|--------|----------|-------------------|
| **Chart** | Trends, comparisons, composition | Chart type (bar/column/line/pie/stacked), X-axis (group / status column / date / person / dropdown), Y-axis (count of items OR sum/avg/min/max/median of a numeric column) |
| **Numbers** | Single KPI | Aggregation (sum/avg/count/median/min/max) of a numeric column; optional **goal** target; optional **comparison** to previous period |
| **Battery** | Status distribution at a glance | Reads a status column; shows % share of each label |
| **Table** | Ranked / detailed list | Columns to show, sort order, filters |

Supporting widgets that exist but are less central here: Funnel (chart-type variant for stage drop-off in some setups), Pie (chart type), Timeline, and text/markdown widgets for labeling sections.

## Chart Widget Axis Choices by Question

| Business question | Chart type | X-axis | Y-axis |
|-------------------|-----------|--------|--------|
| Leads by stage (funnel) | Column / bar | Status column (stage) | Count of items |
| Stage-to-stage conversion | Column | Status column | Count of items (read drop-off between bars) |
| Win rate (Won vs Lost) | Pie | Status column filtered to Won/Lost | Count of items |
| Lost-reason breakdown | Pie / bar | Lost-reason status or dropdown | Count of items |
| Revenue by service type | Bar / column | Service-type dropdown/status | Sum of value column |
| Revenue trend month-over-month | Line | Date column (binned monthly) | Sum of value column |
| Inquiries over time | Line / column | Date column (binned) | Count of items |
| Lead source effectiveness | Column | Source dropdown | Count of items (filter to Won for ROI) |
| Booking volume by service | Column | Service-type dropdown | Count of items |

## Numbers Widget Setups

| KPI | Aggregation | Goal? | Comparison? |
|-----|-------------|-------|-------------|
| Total revenue this month | Sum of value column | Monthly revenue target | vs previous month |
| Expected / forecast value | Sum of value column (filtered to open stages) | Forecast target | optional |
| Deposits collected | Sum of deposit column | — | vs previous period |
| Outstanding balance | Sum of (balance) column | — | — |
| Win rate | Count Won ÷ requires two Numbers or a formula-fed column | Target % | vs previous period |
| Total inquiries | Count of items | Volume goal | vs previous period |

> Note: monday's Numbers widget aggregates a single column. A true ratio like win-rate % is cleanest when the source board carries a **Formula column** computing it, or is shown via a Pie chart of Won vs Lost.

## Typical Source Board Structure (CRM example — doggy-daycare)

| Column | Type | Type ID | Purpose |
|--------|------|---------|---------|
| Lead / Client name | Name (item) | `name` | Item title |
| Stage | Status | `status` | Funnel stage; drives pipeline & conversion charts |
| Won/Lost | Status | `status` | Outcome; drives win-rate pie |
| Lost reason | Status or Dropdown | `status` / `dropdown` | Why deals didn't convert |
| Lead source | Dropdown | `dropdown` | Channel attribution for source ROI |
| Service type | Dropdown or Status | `dropdown` / `status` | Daycare / boarding / grooming split |
| Deal value | Numbers | `numbers` | Summed for revenue charts |
| Deposit collected | Numbers | `numbers` | Deposits KPI |
| Expected revenue | Numbers / Formula | `numbers` / `formula` | Forecast |
| Inquiry date | Date | `date` | X-axis for volume/revenue trend |
| Close date | Date | `date` | Time-frame for won-revenue trend |
| Owner | People | `people` | Optional segmentation |

### Status label JSON — Stage column
```json
{
  "labels": {
    "0": "New Inquiry",
    "1": "Contacted",
    "2": "Tour Scheduled",
    "3": "Trial Day",
    "4": "Won",
    "5": "Lost"
  }
}
```

### Status label JSON — Won/Lost column
```json
{
  "labels": {
    "1": "Won",
    "2": "Lost"
  }
}
```

### Status label JSON — Lost reason column
```json
{
  "labels": {
    "0": "Price too high",
    "1": "Chose competitor",
    "2": "No availability",
    "3": "Went silent",
    "4": "Not a fit"
  }
}
```

## Example Dashboard: Doggy-Daycare Owner View

Story: **Pipeline & revenue health.** Audience: owner. Default filter: this quarter (on Inquiry date / Close date as appropriate per widget).

1. **Numbers** — Total revenue (sum of Deal value, filtered to Won, close date this quarter) + goal + vs last quarter.
2. **Numbers** — Total inquiries (count, Inquiry date this quarter) + vs last quarter.
3. **Chart (column)** — Leads by stage: X = Stage, Y = count. Funnel health.
4. **Chart (pie)** — Win rate: Won vs Lost, count.
5. **Chart (bar)** — Revenue by service type: X = Service type, Y = sum of Deal value.
6. **Chart (pie)** — Lost-reason breakdown: X = Lost reason, Y = count (filtered to Lost).
7. **Chart (line)** — Revenue trend: X = Close date (monthly), Y = sum of Deal value.

## Limitations & Honest Constraints

- **Ratios/percentages** (win rate, conversion %) aren't a native single-widget aggregation. Use a Pie chart for share, or add a **Formula column** on the source board and surface it via Numbers/Table. Chart Y-axis cannot itself compute "count A ÷ count B."
- **Chart Y-axis must be numeric** for sums/averages — you cannot sum a text or status column, only count items grouped by it.
- **Date binning** (week/month/quarter) is available on Chart date axes but exact granularity options depend on the chart configuration.
- **Numbers comparison** compares to the immediately prior equivalent period; custom baselines aren't freely definable.
- **Widget count per dashboard and number of boards you can source into one dashboard are plan-dependent** (higher tiers allow more boards per dashboard). Confirm the account's plan before promising many-board dashboards.
- **Dashboards read live board data** — they don't store historical snapshots. If a column value changes, past charts reflect the current state, not what it was at the time (unless a date column freezes the event).
- **Cross-board charts require compatible columns** — the same status labels / dropdown values / column types must exist across sourced boards for a combined chart to aggregate correctly.
- **Battery widget** only reflects a status column's current distribution; it is not a trend tool.
- This specialist covers **analytical** views only. "Due today," "overdue," "my open tasks," and action-now triage belong to the **operational-dashboards** specialist.
