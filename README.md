# NFL Stats Hub 🏈

An interactive NFL standings dashboard built entirely through agentic coding with Claude AI. No manual code was written — every file in this repository was generated through a conversation with Claude.

---

## What It Does

- **Standings table** — all 32 teams with W/L record, win percentage, points for/against, point differential, home/away splits, and current streak
- **Sortable columns** — click any column header to sort ascending or descending
- **Conference & division filters** — toggle between AFC/NFC and filter by East/North/South/West
- **Top 10 scoring chart** — bar chart of the highest-scoring teams in the current filter
- **Point differential leaderboard** — visual bar display of the best and worst differentials
- **NFL News section** — AI-powered live news feed (see note below)

---

## Project Structure

```
nfl-dashboard/
├── index.html           # Self-contained dashboard (all HTML, CSS, JS in one file)
├── fetch_data.py        # Python script to pull live standings from ESPN API
├── data/
│   └── nfl_stats.json   # Standings data (synthetic sample included)
├── transcript/
│   └── claude_chat.md   # Full Claude conversation log used to build this project
└── README.md
```

---

## How to Run

### Option 1 — Open directly in a browser (no setup needed)
The dashboard has synthetic standings data baked in. Just open `index.html` in any browser and everything renders immediately — no server, no installs, no API keys.

### Option 2 — Refresh with live ESPN data
Run the Python fetcher to overwrite the embedded data with real current standings:

```bash
python fetch_data.py
```

This hits the ESPN public API (no key required) and saves fresh data to `data/nfl_stats.json`. The dashboard will prefer that file when served from a local server:

```bash
# Any simple local server works, e.g.:
python -m http.server 8000
# then open http://localhost:8000
```

---

## Why the NFL News Section Only Works Inside Claude.ai

The news feed at the bottom of the dashboard is powered by the **Anthropic Messages API** with web search enabled. When Claude fetches live headlines, it calls:

```
POST https://api.anthropic.com/v1/messages
```

This requires a valid Anthropic API key passed in the request headers. Normally that means embedding a key like this in the JavaScript:

```js
headers: {
  "x-api-key": "sk-ant-...",   // ← this is the problem
  "Content-Type": "application/json"
}
```

**We deliberately did not do this.** Here's why:

### The API key problem in a purely client-side app

This project was built entirely through Claude — no backend, no build pipeline, no deployment infrastructure. It is a single HTML file meant to be previewed directly in a browser or hosted statically on GitHub Pages / htmlpreview.github.io.

In that context, any API key placed inside `index.html` is **fully visible to anyone who views the page source**. There is no server to hide it behind, no environment variable system, and no secrets manager. Publishing a real Anthropic API key in a public GitHub repository would expose it to the entire internet, allowing anyone to use it — racking up costs or hitting rate limits — before Anthropic's automated scanners even had a chance to flag it.

Rather than include a compromised key or build backend infrastructure that fell outside the scope of this project, the news section was designed to work **exclusively within Claude.ai's own preview environment**, where Anthropic handles authentication automatically on the server side. No key ever touches the client.

### What you see depending on where you open the file

| Environment | Standings & Charts | NFL News |
|---|---|---|
| Claude.ai preview | ✅ Works | ✅ Works (auth handled by Anthropic) |
| `htmlpreview.github.io` | ✅ Works | ⚠️ Shows graceful error message |
| Local file (`file://`) | ✅ Works | ⚠️ Shows graceful error message |
| Local server (`localhost`) | ✅ Works | ⚠️ Shows graceful error message |

The dashboard degrades gracefully — the news section shows an explanatory message rather than breaking anything else on the page.

### How you could make it work everywhere

If you wanted the news feed to work on a public deployment, the right approach is a small **serverless backend** that holds the API key securely and proxies requests from the browser. Options include:

- A [Vercel Edge Function](https://vercel.com/docs/functions)
- A [Netlify Function](https://docs.netlify.com/functions/overview/)
- A [Cloudflare Worker](https://workers.cloudflare.com/)

The browser would call your own endpoint (e.g. `/api/news`) instead of Anthropic directly, and your function would attach the key server-side before forwarding the request. The key would never be visible to the client.

That said, building that infrastructure was out of scope for a project created purely through agentic coding in Claude — so we kept it honest and documented the limitation instead.

---

## Data Source

Standings data is fetched from the **ESPN public API** — no key required:

```
https://site.api.espn.com/apis/v2/sports/football/nfl/standings
```

The `data/nfl_stats.json` file included in this repo contains synthetic data modeled on a realistic NFL season and is used as a fallback when the live API is not available.

---

## How This Was Built

Every line of code in this repository was generated by Claude (claude.ai) through a natural language conversation. No code was written by hand. The workflow:

1. Described the project goal to Claude in plain English
2. Claude generated each file iteratively based on prompts
3. Errors and layout issues were fixed by describing the problem back to Claude
4. Claude diagnosed and patched each issue in subsequent turns

The full conversation transcript is saved in `transcript/claude_chat.md`.

---

## Agentic Coding Tools Used

- **Claude (claude.ai)** — code generation, debugging, and iteration
- **ESPN Public API** — live NFL standings data
- **Anthropic Messages API** — AI-powered news feed (Claude.ai preview only)
- **Chart.js** — bar chart rendering
- **Google Fonts** — Barlow Condensed / Barlow typefaces
