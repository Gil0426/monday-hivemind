# monday.com Hivemind

An AI-powered board design assistant for monday.com. Describe what you need — the Hivemind
routes your request to the right specialist, reads real monday.com documentation, and returns
a complete board plan before anything is written.

Works from the terminal or directly inside the Claude desktop app.

---

## What you need before starting

- **Python 3.10 or higher** — check with `python3 --version`
- **Git** — to clone the repo
- **An Anthropic API key** — [get one here](https://console.anthropic.com/) (free to sign up, pay per use — a typical board design costs a few cents)

---

## Installation

### 🐧 Linux

```bash
# 1. Clone the repo
git clone https://github.com/Gil0426/monday-hivemind.git
cd monday-hivemind

# 2. Create a virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Add your API key
cp .env.example .env
nano .env   # replace the placeholder with your key: ANTHROPIC_API_KEY=sk-ant-...

# 4. Run it
./run.sh
```

---

### 🍎 macOS

```bash
# 1. Clone the repo
git clone https://github.com/Gil0426/monday-hivemind.git
cd monday-hivemind

# 2. Create a virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Add your API key
cp .env.example .env
open -e .env   # opens in TextEdit — replace the placeholder with your key

# 4. Run it
./run.sh
```

> If `python3` is not found, install it via [python.org](https://python.org) or Homebrew: `brew install python`

---

### 🪟 Windows

Pick the option that matches your setup:

#### Option A — PowerShell (native Windows)

```powershell
# 1. Clone the repo
git clone https://github.com/Gil0426/monday-hivemind.git
cd monday-hivemind

# 2. Create a virtual environment and install dependencies
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# 3. Add your API key
copy .env.example .env
notepad .env   # replace the placeholder with your key: ANTHROPIC_API_KEY=sk-ant-...

# 4. Run it
.\run.bat
```

> If `python` is not found, download it from [python.org](https://python.org) — check **"Add Python to PATH"** during install, then restart your terminal.

#### Option B — WSL / Ubuntu (Windows Subsystem for Linux)

If you're using WSL, follow the Linux steps above exactly — it runs identically.

```bash
git clone https://github.com/Gil0426/monday-hivemind.git
cd monday-hivemind
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env   # add your API key
./run.sh
```

---

## Getting your Anthropic API key

1. Go to [console.anthropic.com](https://console.anthropic.com/) and sign in (or create a free account)
2. Click **API Keys** in the left sidebar
3. Click **Create Key**, give it a name like `monday-hivemind`, and copy it
4. Paste it into your `.env` file:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

> **Keep your key private.** Never share it in chat, commit it to a public repo, or post it publicly.
> If you accidentally expose it, go to the Console, revoke it immediately, and create a new one.

---

## Running it daily

**Linux / macOS:**
```bash
./run.sh
```

**Windows (PowerShell):**
```powershell
.\run.bat
```

**From anywhere — add an alias so you can type `hivemind` in any terminal:**

Linux / macOS (add to `~/.zshrc` or `~/.bashrc`):
```bash
alias hivemind='bash /path/to/monday-hivemind/run.sh'
```

Windows PowerShell (add to your PowerShell profile):
```powershell
Set-Alias hivemind "C:\path\to\monday-hivemind\run.bat"
```

---

## Use from the Claude desktop app (no terminal needed)

Register the Hivemind as an MCP server once and its tools appear natively in every Claude chat.

**Linux / macOS** — edit `~/.config/Claude/claude_desktop_config.json`:
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

**Windows (PowerShell)** — edit `%APPDATA%\Claude\claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "monday-hivemind": {
      "command": "C:\\path\\to\\monday-hivemind\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\monday-hivemind\\mcp_server.py"]
    }
  }
}
```

**Windows (WSL)** — edit `%APPDATA%\Claude\claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "monday-hivemind": {
      "command": "wsl",
      "args": [
        "-e",
        "/home/<your-wsl-username>/monday-hivemind/.venv/bin/python",
        "/home/<your-wsl-username>/monday-hivemind/mcp_server.py"
      ]
    }
  }
}
```

After editing, **restart the Claude desktop app**. You'll have three tools available in any chat:

| Tool | What it does |
|---|---|
| `design_board` | Routes your request to the best specialist and returns a full dry-run board plan |
| `list_specialists` | Shows all available specialists |
| `create_specialist` | Generates and saves a new specialist on the fly |

Example prompts:
```
Design a CRM board for a 5-person sales team.
List my available board specialists.
Create a new specialist for marketing campaign tracking.
```

---

## Example terminal session

```
> build I need a board to track vendor contracts — renewal dates, owners, and value

  → Routing to: example-board-builder

  [dry-run board plan]

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

Browse and install individual specialists:
**[github.com/Gil0426/monday-hivemind-specialists](https://github.com/Gil0426/monday-hivemind-specialists)**

---

## Add a specialist

**From the terminal:**
```
> new specialist
```

**From Claude chat (MCP):**
```
Create a specialist for [your domain]
```

**Manually:**
```bash
mkdir specialists/my-specialist
# write specialists/my-specialist/persona.md  ← identity, approach, constraints
# write specialists/my-specialist/reference.md ← column types, board structures, limitations
```

Specialists are picked up automatically on next run — no registration needed.
Commit the folder to share with your team.

---

## Upload a document

Drop `.txt` or `.pdf` files into `inputs/` to use them as requirements:

```
> build --doc inputs/brief.pdf Build this board
```

---

## Project layout

```
monday-hivemind/
├── run.sh / run.bat            ← launchers (Linux/macOS / Windows)
├── mcp_server.py               ← Claude desktop app integration
├── manager/
│   └── manager.py              ← terminal interface
├── shared/                     ← stable engine (don't edit without team review)
├── specialists/
│   └── <name>/
│       ├── persona.md          ← specialist identity + constraints
│       └── reference.md        ← monday.com grounding doc
├── inputs/                     ← drop requirement documents here
├── references/                 ← shared team reference docs
└── .env.example                ← copy to .env and add your API key
```

---

## How it works

```
You → Manager → routes to Specialist → reads docs → designs board → dry-run plan
```

The Manager routes your request to the best specialist. The specialist reads its grounding
documentation (real monday.com docs, not guesses) and outputs a complete dry-run plan —
every board, group, column, and sample item — before anything is written to monday.com.
