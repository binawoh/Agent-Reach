---
name: agent-reach
description: >
  Route internet research, web search and URL reading to the current agent's
  built-in tools, external search, platform-specific channels, page extraction
  or host browser tools. Covers news, official sources, social posts, video
  transcripts and RSS. Fetch and verify content; not for posting or other
  write operations. Prefer a dedicated platform skill when one is available.
metadata:
  homepage: https://github.com/binawoh/Agent-Reach
---

# Agent Reach — internet capability router

Choose capabilities by task, then call public interfaces available in the current
environment. Agent Reach is the router; Exa and other search services are backends.

## Cost boundary

Use only capabilities verified to be free or included without additional charges.
An API key, balance or promotional credit does not prove this. **TinyFish is limited
to free Search / Fetch. Never invoke its Agent, Agent Batch, Browser or browser-session
creation through CLI, MCP, API or another skill.** Failed Fetch, promotional credits
or a generic request to use TinyFish do not authorize paid features. If cost is unknown
or the free allowance is exhausted, use another verified free channel or report the
gap. Do not top up, upgrade or consume paid balance automatically.

## Standing rules (apply for the whole session)

1. **Health-check before acting**: for multi-backend/login-backed platforms (XiaoHongShu /
   Reddit / Bilibili / Twitter / Facebook / Instagram), run `agent-reach doctor --json` first.
   Use a populated `active_backend`; `active_backend: null` means Doctor deliberately skipped a
   live probe to avoid browser-cookie reads or remote writes, not that no backend exists. Only when
   the user's task requires that platform, run the reference's read-only command to verify it.
2. **Announce what you use**: say "using agent-reach, platform X via backend Y"
   before starting.
3. **On failure, follow the retry chains in references/** — never guess
   commands.
4. **Expand to meet evidence needs**: start with primary sources; add relevant
   social platforms when the task needs people's experiences. Stop when evidence
   is sufficient. Stale results, unrelated pages and homepage-only links require
   refinement or another channel even if the command succeeded; see [search](references/search.md).
5. **Personal maintenance**: retain the fork's weekly upstream sync and follow
   [personal maintenance](references/personal-maintenance.md) for local updates.
   Do not add update checks or installations after each search.

## Routing table

Discover the current skill location, session-provided search/read/browser tools,
loaded MCP tools, installed commands and their configuration at runtime. Discover
only what this task needs. A host named Codex or Claude does not prove that search
is available. Do not assume a username, drive, checkout path or agent.
The bundled PowerShell search script is optional; call available public MCP/CLI/API
interfaces directly or write an adapter while preserving task-based routing and keeping
credentials local. A missing fixed directory is not a reason to reinstall.
When Firecrawl CLI is needed, install it if missing and complete authentication if
unauthenticated. Verify authentication before searching;
follow [Firecrawl CLI setup](references/search.md#firecrawl-cli-准备). Do not skip
the backend just because its CLI has not been installed yet.

| User intent | Preferred capability | Details |
|---------|------|---------|
| General web search, newly published news/announcements | Built-in search; external search if unavailable or insufficient | [search](references/search.md) |
| Official documents, technical sources, financial reports | Exa; cross-check with built-in search as needed | [search](references/search.md) |
| Known URL, full text or tables | Built-in reader if sufficient; Firecrawl for full extraction | [web](references/web.md) |
| Content requiring expansion, pagination or interaction | Existing host browser tools without additional charges | [web](references/web.md) |
| XiaoHongShu / Twitter / Bilibili / V2EX / Reddit / Facebook / Instagram posts | Platform-specific channel | [social](references/social.md) |
| Jobs / LinkedIn / Boss Zhipin | Platform-specific channel | [career](references/career.md) |
| Exact GitHub repository / code lookup | GitHub tools | [dev](references/dev.md) |
| YouTube / Bilibili / podcast transcripts | Transcript channel | [video](references/video.md) |
| Xueqiu / stock quotes | Market or platform channel | [finance](references/finance.md) |
| RSS | feedparser | [web](references/web.md) |

Honor an explicitly requested provider. If blocked or insufficient, explain why
another source is added and label it correctly. Tavily is an external search
alternative; Firecrawl Search and TinyFish Search are also available as needed.
Search, page extraction and browser-agent execution are different operations.

## Common commands (select the capability first)

```bash
# Optional PowerShell external-search helper: select a provider for the task
agent-search -Query "query" -Limit 5 -Provider exa
agent-search -Query "query" -Limit 5 -Provider tinyfish

# Extract text (complete CLI setup and authentication from search.md first)
firecrawl scrape "https://example.com/article" --format markdown --only-main-content

# GitHub search
gh search repos "query" --sort stars --limit 10

# YouTube subtitles (never use yt-dlp for Bilibili; retry chain in video.md)
yt-dlp --write-sub --write-auto-sub --skip-download -o "/tmp/%(id)s" "URL"

# V2EX hot topics
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"

# Bilibili search (bili-cli, no login needed)
bili search "query" --type video -n 5
```

## Login-backed platforms (pick by doctor's active_backend)

Twitter boundary: cookies saved by `agent-reach configure twitter-cookies`
are used only by `doctor` to check whether explicit credentials are present.
`doctor` does not run `twitter status` or configure the current shell. Before
calling `twitter` directly, explicitly provide `TWITTER_AUTH_TOKEN` and
`TWITTER_CT0` in the child-process environment without logging their values.

XiaoHongShu boundary: Agent Reach must not log the user in or read browser
cookies. OpenCLI may use only an existing Chrome session explicitly controlled
by the user. If none exists, do not automate login; use a manual Cookie-Editor
export with xiaohongshu-mcp or a legacy tool instead.

```bash
# Twitter search (twitter-cli preferred; retry chain in social.md)
twitter search "query" -n 10

# Reddit (NO zero-config path — OpenCLI or rdt-cli, login required)
opencli reddit search "query" -f yaml   # desktop
rdt search "query" --limit 10            # legacy/server

# XiaoHongShu (desktop prefers OpenCLI)
opencli xiaohongshu search "query" -f yaml

# Facebook / Instagram (desktop OpenCLI, browser session)
opencli facebook search "query" -f yaml
opencli facebook groups -f yaml
opencli instagram search "query" -f yaml       # user search
opencli instagram user USERNAME -f yaml        # recent posts from one user
```

## Environment check

If the command is missing from PATH, discover the actual package manager,
environment or entry point; do not assume a named conda environment. Built-in
search alone does not require this check.

```bash
# Channel availability + which backend serves each platform
agent-reach doctor --json
```

When the user asks “help me configure Boss Zhipin” / “帮我配 Boss直聘”, read the
Boss section in `references/career.md`. After explicit install approval, run
`agent-reach install --env=local --system --channels=boss`, launch the dedicated
loopback-only Chrome profile for their OS, then **pause and have the user visually
confirm** the window is logged in (avatar in the top-right); if not, have them log
in manually. Then verify with `boss --cdp-url http://localhost:9222 login --cdp`
and `agent-reach doctor`. Do not make the user assemble CDP flags.
Keep reusing the dedicated Chrome profile; do not recreate it for every run or
switch to the user's daily profile by default. Search with
`boss --browser-source existing-browser --cdp-url http://localhost:9222 search ...`.
On `ENVIRONMENT_RISK`, stop without refreshing, relogging, or retrying.

**Do not trust `boss status` for CDP browser login state** — it only validates the
local `~/.boss-agent/auth/session.enc` store, which does not represent the
dedicated Chrome profile's cookies that `existing-browser` searches actually use. Use
the browser `wt2` cookie probe in `agent-reach doctor` plus the user's visual
confirmation. Never judge login state from the page URL: `security-check` /
`zhipin-security` / `_security_check` pages are anti-bot challenges that appear
even when logged in. `AUTH_EXPIRED` from a search is the ground truth for a
logged-out browser — go straight to the login flow + `login --cdp` instead of
interpreting it as a security check.

## Discovering OpenCLI adapters

When the routing table lacks a needed platform or command, run `opencli list`,
then inspect `opencli <platform> --help`. Discovery proves only that an adapter
exists, not that authentication or target content works. Run read-only commands
only when the user's task requires that platform, and require non-empty content.

## Workspace rules

Use the system or workspace-designated temporary directory and clean up this
task's intermediate files. Use actual tool config directories for persistent
settings; place deliverables according to the user's workspace rules. Never put
cookies, API keys or browser data in skills, source control, logs or responses.

## Detailed references

Read the matching file when you need specifics (commands above cover the
common cases; references hold per-backend command groups, caveats, retry
chains — note: reference docs are written in Chinese, commands are universal):

- [Search](references/search.md) — built-in/external search and result validation
- [Social](references/social.md) — XiaoHongShu, Twitter, Bilibili, V2EX, Reddit, Facebook, Instagram (multi-backend/login-backed groups)
- [Career](references/career.md) — LinkedIn
- [Dev](references/dev.md) — GitHub CLI
- [Web](references/web.md) — built-in reading, Firecrawl, TinyFish Fetch, host browser, RSS
- [Video](references/video.md) — YouTube, Bilibili, Xiaoyuzhou
- [Finance](references/finance.md) — Xueqiu quotes, search and market content

## Configure a channel

If a channel needs setup, fetch the install guide:
https://raw.githubusercontent.com/binawoh/Agent-Reach/main/docs/install.md

The user only provides cookies / one extension click; the agent does the rest.
