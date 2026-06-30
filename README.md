# monday.com Hivemind

A team-maintained system of AI specialists that design monday.com boards faster and more
accurately than monday's native AI. Each specialist is grounded in real monday.com
documentation, not guessing.

---

## Quick Start

```bash
git clone https://github.com/Gil0426/monday-hivemind.git
cd monday-hivemind

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# open .env and add your ANTHROPIC_API_KEY

./run.sh
```

That's it. You'll see the specialist menu and a command prompt.

---

## Daily use

**From the terminal:**
```bash
# from inside monday-hivemind/
./run.sh
```

**From anywhere (add to `~/.zshrc` or `~/.bashrc`):**
```bash
alias hivemind='bash /home/giloliveira/Documents/Monday\ Board\ Builders/monday-hivemind/run.sh'
```
Then just type `hivemind` in any terminal window.

---

## Use from the Claude desktop app

Register the MCP server once and the tools appear natively inside Claude — no terminal needed.

**1. Register the server** — add this block to `~/.config/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "monday-hivemind": {
      "command": "/full/path/to/monday-hivemind/.venv/bin/python",
      "args": ["/full/path/to/monday-hivemind/mcp_server.py"]
    }
  }
}
```

**2. Restart the Claude desktop app.**

**3. Use it in chat** — Claude now has three tools from the hivemind:

| Tool | What it does |
|---|---|
| `design_board` | Takes a description, routes to the best specialist, returns a full dry-run plan |
| `list_specialists` | Shows available specialists and their domains |
| `create_specialist` | Generates and saves a new specialist on the fly |

Example prompts in Claude chat:
```
Design a CRM board for a 5-person sales team tracking deals, contacts, and pipeline value.

List my available board specialists.

Create a new specialist for marketing — campaign tracking, content calendars, and social media.
```

---

## Example terminal session

```
> build I need a board to track vendor contracts — renewal dates, owners, and value

  → Routing to: example-board-builder

  [full dry-run board plan]

> build --doc inputs/brief.pdf Build a CRM pipeline for our sales team

  → Routing to: crm

  [reads the PDF, outputs a board plan]

> new specialist

  Specialist name: marketing
  Describe what 'marketing' covers: campaign tracking, content calendars, social media

  ✓  specialists/marketing/persona.md
  ✓  specialists/marketing/reference.md
```

---

## Specialists

| Folder | Domain |
|---|---|
| `example-board-builder` | General-purpose boards, one-off trackers |
| `crm` | Contacts, deals, sales pipeline (1- or 3-board CRM) |
| `project-management` | Tasks, timelines, sprints, portfolio tracking |

New specialists are generated on demand and saved to disk — commit them to share with the team.

### Specialist library

Pre-built specialists are available as standalone markdown files — teammates can grab just
the one they need without cloning the full hivemind:

**https://github.com/Gil0426/monday-hivemind-specialists**

```bash
# Install a specialist into your hivemind (from inside monday-hivemind/):
git clone https://github.com/Gil0426/monday-hivemind-specialists /tmp/mh-lib
cp -r /tmp/mh-lib/crm specialists/
rm -rf /tmp/mh-lib
```

---

## Add a specialist

### From the terminal manager
```
> new specialist
```

### From Claude chat (MCP)
```
Create a specialist for [your domain]
```

### Manually
```bash
mkdir specialists/my-specialist
# write specialists/my-specialist/persona.md  ← identity, approach, constraints
# write specialists/my-specialist/reference.md ← column types, board structures, limitations
```

Everything in `reference.md` must come from https://support.monday.com or https://developer.monday.com.
The manager and MCP server pick up new specialists automatically — no registration needed.

---

## Upload a document

Drop `.txt` or `.pdf` files into `inputs/` and reference them:

**Terminal:**
```
> build --doc inputs/brief.pdf Build this board
```

**Claude chat:**
```
Design a board from this document: inputs/brief.pdf
```

---

## Project layout

```
monday-hivemind/
├── run.sh                      ← terminal launcher (use this daily)
├── mcp_server.py               ← Claude desktop app integration
├── manager/
│   └── manager.py              ← terminal REPL
├── shared/
│   ├── agent_loop.py           ← stable engine; don't edit without team review
│   ├── document_reader.py
│   ├── monday_tools.py
│   └── tool_registry.py
├── specialists/
│   └── <name>/
│       ├── persona.md          ← specialist identity + constraints
│       └── reference.md        ← monday.com grounding doc for this domain
├── references/                 ← shared curated docs (PDFs, notes)
├── inputs/                     ← drop requirement documents here
├── requirements.txt
└── .env.example
```

---

## How it works

```
You → Manager/Claude → routes to Specialist → reads persona + reference → designs board → dry-run plan
```

The Manager and MCP server both route your request to the best specialist. The specialist
reads its grounding documentation (real monday.com docs, not guesses), designs the board
using valid column types and structures, and outputs a complete dry-run plan before anything
is written to monday.com.
