# monday-ai — Reference

## Column Types (with API type identifiers)
These are the column types most relevant to AI input/output. The `type` value is what monday's API/columns reference.

| Column | API `type` | Role in AI workflows |
|---|---|---|
| Text | `text` | Short raw input or short AI output (single line) |
| Long Text | `long_text` | Primary target for AI summaries, drafts, extractions; also raw pasted input |
| Status | `status` | AI classification target — fixed label set (color-coded) |
| Dropdown | `dropdown` | AI multi-tag/category target — supports multiple selected labels |
| People | `people` | Owner assignment (set by automation, often after AI triage) |
| Numbers | `numbers` | Scores, counts (better via formula than AI when deterministic) |
| Date | `date` | Deadlines/timestamps (use automation/formula, not AI) |
| Formula | `formula` | Deterministic logic — preferred over AI for math/string rules |
| Connect Boards | `board_relation` | Links items across boards to give agents context |
| Mirror | `mirror` | Surfaces connected-board data (read-only reflection) |
| Dropdown/Tags | `tags` | Cross-board shared tags |

> Note: monday occasionally adjusts internal type strings. Verify against the current API schema before building integrations. Values above reflect commonly used identifiers.

## monday AI Capabilities (real features only)

### 1. AI Blocks (on-board AI actions)
Built-in actions you run on board content:
- **Summarize** — condense long updates / item threads into a field.
- **Categorize / Classify** — map item text to a status or dropdown label.
- **Extract information** — pull entities/values from text into structured columns.
- **Detect sentiment** — classify tone (e.g., positive/neutral/negative) into a status.
- **Translate** — convert text between languages.
- **Generate / Draft text** — produce draft replies, descriptions, summaries.

Wiring rule: choose the **output column type** to match the block — summaries/drafts → `long_text`; categories → `status` or `dropdown`; sentiment → `status`.

### 2. AI-Powered Automations
Pattern: **Trigger → AI action → Column update**.
- *When an item is created → run AI categorize → set Status.*
- *When an update is posted → run AI summarize → write to Long Text.*
- *When Status changes to "Needs triage" → run AI classify priority → set Priority status.*
Keep one AI action per recipe for reliability and easier debugging.

### 3. monday AI Agents (Digital Workforce)
Scoped agents attached to boards that act within defined triggers, knowledge sources, and guardrails:
- **Intake agent** — reads incoming request text, populates structured fields.
- **Triage agent** — assigns owner (People) and priority (Status) based on content.
- **Assistant agent** — drafts responses / suggests next steps into a Long Text field.
Each agent needs: a trigger, defined knowledge sources (boards/docs it may read), explicit allowed actions, and a human-review checkpoint for sensitive decisions.

## Example Board Structure — AI Request Intake & Triage

**Groups**
- `New / Unprocessed`
- `Triaged`
- `In Progress`
- `Resolved`

**Columns**
| Name | Type | Purpose |
|---|---|---|
| Request (Raw) | `long_text` | Untouched incoming text — AI reads, never writes |
| AI Summary | `long_text` | AI summarize output |
| Category | `status` | AI classify output |
| Sentiment | `status` | AI sentiment output |
| Priority | `status` | AI/triage output |
| Owner | `people` | Set by triage agent/automation |
| Suggested Reply | `long_text` | Assistant agent draft |
| Related Account | `board_relation` | Context for agents |
| Reviewed? | `status` | Human checkpoint |

**AI wiring**
- AI Block (Summarize): Request (Raw) → AI Summary.
- Automation: *When item created → AI categorize Request (Raw) → set Category.*
- Automation: *When Category set → AI detect sentiment → set Sentiment.*
- Triage agent: reads Request (Raw) + Related Account → sets Priority + Owner.
- Assistant agent: drafts Suggested Reply (human edits before sending).
- Automation: *When item moves to Triaged → set Reviewed? to "Pending".*

## Status Label JSON Examples
Use these as starting label sets so AI has a fixed vocabulary.

**Category**
```json
{
  "labels": {
    "0": "Bug / Issue",
    "1": "Feature Request",
    "2": "Billing",
    "3": "How-to / Support",
    "4": "Other"
  },
  "labels_colors": {
    "0": "#e2445c",
    "1": "#0086c0",
    "2": "#fdab3d",
    "3": "#00c875",
    "4": "#c4c4c4"
  }
}
```

**Sentiment**
```json
{
  "labels": {
    "0": "Positive",
    "1": "Neutral",
    "2": "Negative"
  },
  "labels_colors": {
    "0": "#00c875",
    "1": "#c4c4c4",
    "2": "#e2445c"
  }
}
```

**Priority**
```json
{
  "labels": {
    "0": "Urgent",
    "1": "High",
    "2": "Medium",
    "3": "Low"
  },
  "labels_colors": {
    "0": "#e2445c",
    "1": "#fdab3d",
    "2": "#0086c0",
    "3": "#c4c4c4"
  }
}
```

**Reviewed?**
```json
{
  "labels": {
    "0": "Pending",
    "1": "Approved",
    "2": "Needs Edit"
  },
  "labels_colors": {
    "0": "#fdab3d",
    "1": "#00c875",
    "2": "#e2445c"
  }
}
```

## Limitations & Honest Notes
- **Plan & credits:** AI features require eligible plans and consume AI credits/usage; high-volume automations can exhaust allotments. Confirm the client's tier and limits.
- **Enablement:** AI may need admin/account-level activation and can vary by region. Verify before promising availability.
- **Accuracy is probabilistic:** Classification, summarization, and sentiment can be wrong. Always include a human-review status for high-stakes routing.
- **Free-text quality matters:** Garbage input → garbage AI output. Keep raw input clean and separate from AI output.
- **No deterministic math:** Use `formula` columns for calculations, dates, and rule-based logic — not AI.
- **Agent scope is bounded:** Agents act only within configured triggers, knowledge sources, and permitted actions; they are not autonomous.
- **Data sensitivity:** Restrict which boards/columns AI can read when handling confidential or regulated data.
- **Verify feature names/IDs:** monday's AI feature set and API identifiers evolve — confirm against current monday.com documentation before final build.
