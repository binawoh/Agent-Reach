---
name: use-tinyfish
description: Use TinyFish Search and Fetch when the user requests TinyFish or the task router selects it for web search or URL reading. Free functions only; never use TinyFish Agent, Agent Batch or Browser.
---

# TinyFish Search and Fetch

This is the personal free-only replacement for an installed `use-tinyfish` skill.
If agent-reach is available, discover its current skill and follow its task routing
and cost boundary. Do not assume a fixed installation path or replace the host's
built-in search for every web request.

## Cost boundary

Only use Search and Fetch when verified to be free. An API key, balance, trial or
promotional credit is not permission to consume paid features. Never invoke
TinyFish Agent, Agent Batch, Browser or create a browser session, whether through
CLI, MCP, API, scripts or another skill. Do not run paid features for testing.
If pricing or the remaining free allowance is uncertain, use another verified free
channel or report the gap. Do not top up or upgrade automatically.

## Setup

Discover an existing CLI or loaded MCP and its current public schema/help. If the
CLI is needed and missing, install the official package:

```bash
npm install -g @tiny-fish/cli
```

Reuse local authentication. If needed, inspect `tinyfish auth login --help` and
start the supported login flow; browser sign-in may require the user to finish.
Never print or commit API keys. New MCP tools load in a new agent session; do not
reinstall solely because they are missing from the current one. Repairs marked
`unattended_safe: false` must be shown to the user instead of executed automatically.

## Search and Fetch

No URL: Search, then Fetch only the sources needed. Known URL: Fetch directly.
Use current help if parameters differ from these examples:

```bash
tinyfish search query "query"
tinyfish fetch content get --format markdown "https://example.com/article"
```

Check relevance, source URL, publication/event date and the requested content.
Homepage-only search results or empty/incomplete Fetch output are insufficient.
For incomplete or dynamic pages, use another verified free reader or the host's
existing browser without additional charges. Never escalate to TinyFish's paid
tools. If no allowed path works, state what could not be verified.

Respond in the user's language and cite the specific original pages. Keep
credentials and sensitive debug output private.
