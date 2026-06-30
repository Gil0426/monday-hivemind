# monday.com Hivemind

A team-maintained system of AI specialists that design monday.com boards faster and more
accurately than monday's native AI. Each specialist is grounded in real monday.com
documentation, not guessing.

---

## How it works

```
You → Manager → routes to Specialist → reads persona + reference → designs board → dry-run plan
```

The **Manager** is the only interface you talk to. Describe what board you need. The Manager
routes to the best **Specialist**. The specialist reads its grounding documentation, designs
the board using real monday.com column types and structures, and outputs a complete dry-run
build plan — every board, group, column, and sample item — before anything is written.

---

## Specialists

| Folder | Domain |
|---|---|
| `example-board-builder` | General-purpose boards, one-off trackers |
| `crm` | Contacts, deals, sales pipeline (1- or 3-board CRM) |
| `project-management` | Tasks, timelines, sprints, portfolio tracking |

New specialists can be generated on demand from inside the Manager and saved to this repo.

---

## Setup

### Requirements

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)

### Install

```bash
git clone <your-repo-url>
cd monday-hivemind

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# then edit .env and add your ANTHROPIC_API_KEY
```

Load the env before running:

```bash
export $(cat .env | xargs)       # bash/zsh
# or use direnv, python-dotenv, etc.
```

---

## Run

```bash
# from monday-hivemind/
python -m manager.manager
```

You'll see the specialist list and a command prompt.

### Example session

```
> build I need a board to track vendor contracts — renewal dates, owners, and value

  → Routing to: example-board-builder

  [dry-run board plan appears here]

> build --doc inputs/brief.pdf Build a CRM pipeline for our sales team

  → Routing to: crm

  [reads the PDF, then outputs a board plan]
```

---

## Add a specialist (two ways)

### Way 1 — Generate from the Manager (fast)

```
> new specialist

  Specialist name: marketing
  Describe what 'marketing' covers: campaign tracking, content calendars, social media scheduling

  Generating 'marketing'...
  ✓  specialists/marketing/persona.md
  ✓  specialists/marketing/reference.md
```

Then review the generated files, commit, and push.

### Way 2 — Write it manually (for depth)

```bash
mkdir specialists/my-specialist
touch specialists/my-specialist/persona.md
touch specialists/my-specialist/reference.md
```

**`persona.md`** — Who the specialist is, its approach to board design, and its hard constraints
(what monday.com does NOT support in this domain).

**`reference.md`** — The grounding doc: relevant column types with type IDs, typical board
structures in tables, status label JSON, and documented limitations. Source everything from
https://support.monday.com or https://developer.monday.com.

The Manager picks up new specialists automatically on next run. Commit `specialists/<name>/`
to the repo and your teammates get it on next pull.

---

## Upload a document

Drop `.txt` or `.pdf` files into `inputs/` and pass the path with `--doc`:

```
> build --doc inputs/my-brief.pdf Build this board
```

The specialist reads the document first, then designs the board from its contents.

---

## Project layout

```
monday-hivemind/
├── manager/
│   └── manager.py          ← entry point; never edit shared/ from here
├── shared/
│   ├── agent_loop.py       ← stable engine; changes need team review
│   ├── document_reader.py
│   ├── monday_tools.py
│   └── tool_registry.py
├── specialists/
│   └── <name>/
│       ├── persona.md      ← specialist identity + constraints
│       └── reference.md    ← monday.com grounding doc for this domain
├── references/             ← shared curated docs (PDFs, notes)
├── inputs/                 ← user-uploaded requirement documents
├── requirements.txt
└── .env.example
```
