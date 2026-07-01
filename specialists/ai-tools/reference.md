# ai-tools — Reference

## monday AI Surfaces: buildability matrix

| Surface | What it is | Buildable via API/MCP? | Primary tooling / path | Credit-consuming? |
|---|---|---|---|---|
| **AI-powered column** | Column-level AI action (rainbow AI star); e.g. Extract Info, Writing assistant, Summarize, Categorize, Translate, Generate docs | **No — UI only** | Column three-dot menu → AI action / "Set a custom prompt" | Yes, per run |
| **AI Blocks** | Reusable single-task AI building blocks (extract, summarize, classify, generate…) powering columns, automations, workflows | Indirectly (via workflows) | 7 monday-AI action blocks inside workflow builder | Yes, per execution |
| **AI workflow** | Visual cross-board/workspace flow chaining triggers + action blocks incl. AI blocks | **Yes** | `plan_workflow` → `create_workflow` (DRAFT) → `update_workflow` → `publish_workflow`; UI at `custom_objects/{id}` | Yes, per AI block run |
| **AI Agent** | Native AI worker monitoring, deciding, executing in a loop | **Yes** | `agent_catalog` (read-only) → `manage_agent` / `manage_agent_triggers` / `manage_agent_skills` / `manage_agent_knowledge` | Yes, per action |
| **AI Assistant** | In-product assistant for Q&A + actions across boards (plus CRM/Service variants) | No (in-product) | monday UI | Yes |

## MCP / API tool map

### Workflows
| Tool | Purpose | Notes |
|---|---|---|
| `plan_workflow` | Decompose plain-English process → workflows, boards/columns, block IDs + Mermaid plan | **Run FIRST** — source of real block IDs |
| `create_workflow` | Create workflow as a **DRAFT** in a workspace | Not live yet |
| `update_workflow` | Configure the draft | — |
| `publish_workflow` | Make the workflow **live** | Required before it runs |

### Agents
| Tool | Purpose | Notes |
|---|---|---|
| `agent_catalog` → `list_triggers` | Discover real trigger `block_reference_id`s | **READ-ONLY** |
| `agent_catalog` → `list_skills` | Discover real skill ids | **READ-ONLY** |
| `manage_agent` | Create (AI prompt or `create_blank`), update plan, activate, run, deactivate, delete | Agents start **INACTIVE** |
| `manage_agent_triggers` | Attach triggers | OAuth/3rd-party (Slack/Gmail/Salesforce) = **UI-configured**, not in catalog |
| `manage_agent_skills` | Attach or author skills | Use catalog ids |
| `manage_agent_knowledge` | Provide reference knowledge | — |

External / BYO agents: connectable as first-class participants via **Managed provider** or **Custom webhook**. Supported models include **Claude** and others exposed by the platform.

## AI-powered column recipe template (UI hand-off)

Since AI columns are **UI-only**, I deliver a recipe a human executes:

```
Board:        [target board name]
Source col:   [column feeding the AI action]
AI column:    [new column name]
Action:       [Extract Info | Writing assistant | Summarize | Categorize | Translate | Generate docs]
Prompt:       "[exact custom prompt text]"
Output cols:  [column(s) that receive extracted/generated values + their types]
Trigger:      [manual run | on item create/change — via automation]
Credits:      Each run deducts AI credits (tracked in account usage dashboard).
Setup path:   Column header three-dot menu → AI actions → [action] / "Set a custom prompt"
```

### Common column types for AI outputs
| Column | Type ID | Typical AI use |
|---|---|---|
| Text | `text` | Short extracted/generated text |
| Long Text | `long_text` | Summaries, drafted content |
| Status | `status` | Categorize / label output |
| Numbers | `numbers` | Extracted amounts (invoice totals) |
| Date | `date` | Extracted dates (due, invoice) |
| Email | `email` | Extracted contact email |
| Phone | `phone` | Extracted phone number |
| Dropdown | `dropdown` | Multi-category classification |
| People | `people` | Assignment from decisioning |
| Doc | `doc` | Generate docs with AI |

### Status label JSON (for categorize/label outputs)
```json
{
  "labels": {
    "0": "Uncategorized",
    "1": "Invoice",
    "2": "Contract",
    "3": "Resume",
    "4": "Other"
  },
  "labels_colors": {
    "0": { "color": "#c4c4c4", "border": "#b0b0b0" },
    "1": { "color": "#00c875", "border": "#00b461" },
    "2": { "color": "#0086c0", "border": "#0079b5" },
    "3": { "color": "#a25ddc", "border": "#9a4fd6" },
    "4": { "color": "#e2445c", "border": "#d63852" }
  }
}
```
> Define the exact label set BEFORE configuring the AI column so its prompt maps outputs to real labels.

## Typical board structures

### Extract-Info intake board (invoices/resumes/contracts)
| Column | Type | Role |
|---|---|---|
| Item name | `name` | Document/record title |
| File | `file` | Uploaded source doc |
| Extracted Vendor | `text` | AI-extracted |
| Amount | `numbers` | AI-extracted |
| Invoice Date | `date` | AI-extracted |
| Category | `status` | AI-categorized |
| Summary | `long_text` | AI-summarized |

### Agent-monitored ops board
| Column | Type | Role |
|---|---|---|
| Item name | `name` | Work item |
| Status | `status` | Agent monitors + updates |
| Priority | `status` | Agent decisioning input |
| Owner | `people` | Agent assignment target |
| Notes | `long_text` | Agent-authored context |

## Limitations & gotchas
- **No public API to create/attach an AI action to a column** — AI columns are UI-only; always produce a recipe.
- **Workflows are drafts on creation** — nothing runs until `publish_workflow`. UI lives at `custom_objects/{id}` (not `workflows/`).
- **Agents are INACTIVE on creation** — must be activated via `manage_agent`.
- **OAuth / 3rd-party triggers** (Slack, Gmail, Salesforce, etc.) **won't appear in `agent_catalog`** and must be connected by the user in the UI.
- **Never invent block/skill/trigger IDs** — always source from `plan_workflow` / `agent_catalog`.
- **Every AI run consumes credits** (columns, blocks, agents) — tracked in the account usage dashboard; call this out in every plan.
- **CRM / Service assistants** are distinct feature sets — check their specific docs before promising behavior.

## Documentation index
**Support / product**
- Get started with monday AI — https://support.monday.com/hc/en-us/articles/11512670770834-Get-started-with-monday-AI
- AI Feature Catalog — https://support.monday.com/hc/en-us/articles/24047211522194-AI-Feature-Catalog
- AI-powered columns — https://support.monday.com/hc
