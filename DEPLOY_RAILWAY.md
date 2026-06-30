# Deploy the hivemind to Railway (stable remote connector)

This gives the hivemind a **permanent public HTTPS URL** so Cowork and Claude chat can
reach it 24/7 — no laptop staying on, no tunnel, no URL that changes on restart.

The same three tools (`design_board`, `list_specialists`, `create_specialist`) are served
over HTTP from `mcp_http.py`. Railway runs that process; your secrets live in Railway's
environment variables and never touch the repo.

> Cost: Railway's Hobby plan is ~$5/month and includes trial credit. A connector that
> idles most of the day costs very little.

---

## Prerequisites

- A [Railway](https://railway.app) account (sign in with GitHub).
- This repo on GitHub (a private fork works — Railway deploys private repos).
- Your `ANTHROPIC_API_KEY`.

---

## Step 1 — Create the project from the repo

1. Railway dashboard → **New Project** → **Deploy from GitHub repo**.
2. Authorize Railway for your GitHub account and pick the repo.
3. Railway detects Python (via `requirements.txt`) and uses the start command from
   `railway.json` / `Procfile`: `python mcp_http.py`. No Dockerfile needed.

## Step 2 — Set environment variables

In the service → **Variables**, add:

| Variable | Value | Notes |
|---|---|---|
| `ANTHROPIC_API_KEY` | `sk-ant-...` | Your key. Stays in Railway, never in the repo. |
| `HIVEMIND_TOKEN` | a long random string | The secret path segment. Generate one below. |

Railway injects `PORT` automatically — **do not set it**; `mcp_http.py` reads it and binds
`0.0.0.0`.

Generate a token (any of these):

```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(24))"
# or PowerShell
powershell -Command "[Convert]::ToBase64String((1..24 | ForEach-Object {Get-Random -Max 256}))"
```

## Step 3 — Get the public URL

1. Service → **Settings** → **Networking** → **Generate Domain**.
2. Railway gives you something like `monday-hivemind-production.up.railway.app`.

## Step 4 — Build the connector URL

The connector URL is the domain **plus the secret path** (`/mcp-<HIVEMIND_TOKEN>`):

```
https://monday-hivemind-production.up.railway.app/mcp-<HIVEMIND_TOKEN>
```

Use the exact same token you set in Step 2. Anyone without the path gets a 404 — keep it private.

## Step 5 — Add it in Cowork / claude.ai

**Settings → Connectors → Add custom connector** → paste the full URL above → Save.

Then in Cowork ask **"list specialists"** — you should get **crm / example-board-builder /
project-management**. Done. This URL never changes unless you delete the Railway domain.

---

## Updating

Push to the repo's deploy branch and Railway redeploys automatically. Specialists you add via
`create_specialist` while running on Railway live on Railway's ephemeral disk — to persist
them, commit the generated `specialists/<name>/` folders to the repo (they ship on the next
deploy). For durable storage across redeploys, attach a Railway volume mounted at `specialists/`.

## Local alternative (no cloud)

Don't want to host it? Run it locally behind a cloudflared quick tunnel instead — see the
**Use from Cowork or cloud chat** section of the [README](README.md). That URL changes on every
restart, which is why Railway is the recommended path for anything you demo or rely on.
