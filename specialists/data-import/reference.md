# Data Import Reference

## Source Format → Parsing Tool

| Format | Primary Tool | Notes |
|---|---|---|
| CSV | pandas `read_csv` | Sniff delimiter (`,` `;` `\t` `|`) and encoding (utf-8, latin-1, cp1252). Watch for BOM. |
| XLSX/XLS | pandas `read_excel` + openpyxl | openpyxl for merged cells, multi-row headers, formatting, multiple sheets. |
| PDF | pdfplumber | `extract_tables()` for structured tables; `extract_text()` for forms/invoices/contracts. Layout-dependent — verify column boundaries. |
| MD/TXT | bash + python | Parse tables, bullet lists, key:value lines from requirement/notes docs. |
| JSON | pandas `json_normalize` | Flatten nested objects; nested arrays → child entities for board_relation. |

## Source Type → monday Column Type Mapping

| Source data | monday column type | Type ID (`type` string) | Notes |
|---|---|---|---|
| Short text, names, codes | Text | `text` | Default for identifiers/labels. |
| Long text, notes, descriptions | Long Text | `long_text` | Use when values exceed ~few hundred chars. |
| Single date | Date | `date` | ISO `YYYY-MM-DD`; optional time. |
| Start + end / range | Timeline | `timeline` | Requires `from` and `to` dates. |
| Money / amount / quantity | Numbers | `numbers` | Strip currency symbols/commas; store numeric. Currency is display-only. |
| Category / stage / small fixed set | Status | `status` | Fixed label set with colors; label index matters. |
| Multi-select / tags / larger set | Dropdown | `dropdown` | Multiple selectable values. |
| Person / owner / assignee | People | `people` | Requires resolving to monday user IDs — often escalate. |
| Yes/No, true/false | Checkbox | `checkbox` | Boolean. |
| Email | Email | `email` | Good dedup key. |
| Phone | Phone | `phone` | |
| URL / link | Link | `link` | Stores url + display text. |
| Rating (1–5) | Rating | `rating` | Integer scale. |
| Location / address | Location | `location` | Lat/lng + address string. |
| Reference to another board's item | Board Relation | `board_relation` | Used to preserve entity relationships. |
| Time-tracking data | Time Tracking | `time_tracking` | Rarely from import. |
| Country | Country | `country` | ISO country codes. |

> Confirm exact `type` strings and settings schema at build time with `get_column_type_info`. Do not hardcode label indices without checking.

## Column Value Formats (for `change_item_column_values`)

Values are passed as a JSON object keyed by column ID. Common shapes:

**Text**
```json
{ "text_col": "Acme Corp" }
```

**Long Text**
```json
{ "long_text_col": { "text": "Full multi-line note here" } }
```

**Numbers** (string form, no symbols)
```json
{ "numbers_col": "1500" }
```

**Date**
```json
{ "date_col": { "date": "2024-06-01", "time": "14:30:00" } }
```

**Timeline**
```json
{ "timeline_col": { "from": "2024-06-01", "to": "2024-06-30" } }
```

**Status** (by label text or index — prefer label)
```json
{ "status_col": { "label": "Active" } }
```

**Dropdown** (by labels)
```json
{ "dropdown_col": { "labels": ["Enterprise", "Priority"] } }
```

**Checkbox**
```json
{ "checkbox_col": { "checked": "true" } }
```

**Email**
```json
{ "email_col": { "email": "jane@acme.com", "text": "Jane" } }
```

**Link**
```json
{ "link_col": { "url": "https://acme.com", "text": "Website" } }
```

**People** (requires numeric monday user/team IDs)
```json
{ "people_col": { "personsAndTeams": [ { "id": 12345678, "kind": "person" } ] } }
```

**Board Relation** (link to items in a connected board)
```json
{ "relation_col": { "item_ids": [ 987654321 ] } }
```

## Status / Dropdown Label Definition (at column creation)

When creating a `status` column, provide labels + colors as JSON in the column settings. Example:
```json
{
  "labels": {
    "0": "New",
    "1": "In Progress",
    "2": "On Hold",
    "3": "Done",
    "4": "Cancelled"
  }
}
```
For `dropdown`, labels are defined similarly:
```json
{
  "settings": {
    "labels": [
      { "id": 1, "name": "Enterprise" },
      { "id": 2, "name": "SMB" },
      { "id": 3, "name": "Startup" }
    ]
  }
}
```
> Always derive the label set from the **distinct values found in the source column** during profiling, then confirm before creating — so imported values map to existing labels instead of silently creating new ones.

## Relationship Import Pattern (parents before children)

For a source with linked entities — e.g. **Owners → Dogs → Bookings**:

1. Build the **Owners** board. Create owner items. **Capture the returned item ID** for each owner (keep a `source_key → monday_id` map).
2. Build the **Dogs** board with a `board_relation` column connected to Owners. Create each dog, then `link_board_items_workflow` to its owner using the captured ID.
3. Build the **Bookings** board with a `board_relation` column connected to Dogs. Create bookings and link to the correct dog.

Never create a child before its parent exists and its ID is known. Rows whose parent key can't be resolved are reported as errors — not linked to a guessed parent.

## De-duplication Approach

- monday.com has **no native dedup** — duplicates are created freely if you don't check.
- Before creating: fetch existing items on the target board and match on the **key field** (item name, email, or a client-chosen key column).
- On match: propose **update** (change columns) or **link** (for relations) instead of **create**.
- Normalize before comparing: trim whitespace, case-fold, standardize date/number formats.
- Coordinate with the **Duplicate finder** agent skill and the **validation** specialist rather than reinventing matching logic.

## Chunking & Limits

- monday API enforces **rate limits and query complexity limits**. Do not create thousands of items in one request loop unbatched.
- Create items and apply column values in **batches** (e.g. 25–100 per cycle) with pacing/retry on transient errors.
- For very wide rows, split column updates rather than sending one oversized mutation.
- Track and report progress across chunks.

## Import Summary (always deliver)

```
Import summary — <board name>
  Rows read:            <n>
  Items created:        <n>
  Items updated:        <n>
  Skipped (duplicate):  <n>
  Relationships linked: <n>
  Errored:              <n>
    - row 42: unresolved parent
