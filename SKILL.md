---
name: marketer-github-codex-radar
description: Find and rank current GitHub repositories, skills, agents, and open-source tools that marketers can use inside Codex for audience insight, creative production, decks, social content, brand systems, research, and workflow efficiency. Use when the user asks for trending GitHub things this week, GitHub tools for marketers, Codex-installable marketing skills, creative AI repositories, or a non-coding GitHub digest filtered for marketing usefulness rather than developer tooling.
---

# Marketer GitHub Codex Radar

Use this skill to produce a current, marketer-focused GitHub shortlist. The goal is not "popular developer repos"; it is "things a marketer can use with Codex or ask Codex to operate."

## Workflow

1. Establish the time window.
   - Default to the last 7 days.
   - State the exact date range in the answer.
   - If the user says "this week" or "latest", verify current data with GitHub or web search.
2. Collect candidates.
   - Search GitHub for active repos updated inside the window.
   - Include direct Codex/skill searches and broader creative/productivity searches.
   - Read the project README or repository metadata for finalists before recommending them.
3. Filter for marketer usefulness.
   - Keep tools for insight, decks, docs, brand, design, social, video, research, publishing, knowledge bases, and light automation.
   - Deprioritize framework libraries, SDKs, coding agents, infrastructure, benchmark repos, and demos unless the marketer use is obvious.
4. Check Codex usability.
   - `install`: repository appears installable because it has a usable `SKILL.md`, skill folder, plugin, package, or clear CLI that Codex can call. This is only an assessment label, not permission to install it.
   - `wrap`: useful standalone app or CLI that would need a small Codex skill wrapper.
   - `reference`: useful as inspiration or a tool to run manually, but not directly installable.
   - `skip`: not suitable for marketer workflows.
   - Do not install, clone, download, or modify any recommended repository after a radar run. The user must decide what to install.
5. Rank and explain.
   - Prefer active projects with real adoption, recent pushes, clear README, usable workflow, and strong marketer relevance.
   - Treat adoption as a first-class signal, not a footnote. Stars, forks, release history, contributor activity, issue/PR activity, and reuse by others are all validation proxies.
   - Do not rank a 0-star / 0-fork repository in the top picks unless it is directly installable as a Codex skill and the README/files prove unusually strong usefulness. Otherwise label it `experimental` or omit it.
   - Prefer established repos with lower update freshness over brand-new unvalidated repos when both solve the same marketer job.
   - If exact weekly star growth is unavailable, say so and use stars, forks, update recency, release activity, README quality, and relevance as proxies.
   - Call out weak validation directly in the "Why it matters" column instead of making unproven projects sound broadly endorsed.

## Search Patterns

Use several narrow searches instead of one broad search:

- `presentation AI pushed:>YYYY-MM-DD`
- `content creation AI pushed:>YYYY-MM-DD`
- `creative AI design agent pushed:>YYYY-MM-DD`
- `marketing automation AI pushed:>YYYY-MM-DD`
- `social media AI publisher pushed:>YYYY-MM-DD`
- `SKILL.md Codex marketing presentation pushed:>YYYY-MM-DD`
- `agent skills creative marketing pushed:>YYYY-MM-DD`

When GitHub search syntax is too narrow, broaden one term at a time and keep the filter honest.

## Optional Ranking Script

Use `scripts/rank_marketer_repos.py` when you have JSON repository metadata from GitHub API/search. It accepts either:

- a JSON array of repo objects, or
- a GitHub search API payload with an `items` array.

Example:

```bash
python scripts/rank_marketer_repos.py --input /tmp/repos.json --limit 12
```

The script produces a Markdown table with relevance categories and a score. Treat it as a first pass, then manually inspect finalists before recommending them.

## Output Format

Return a concise table:

| Rank | Repository | Use | Codex fit | Validation | Why it matters |
| --- | --- | --- | --- | --- | --- |

Use `Use` values such as `insights`, `decks`, `creative`, `social`, `video`, `brand`, `automation`, or `knowledge`.

Use `Codex fit` values:

- `install`
- `wrap`
- `reference`
- `skip`

Use `Validation` values:

- `strong`: meaningful stars/forks, active maintainers, releases, or visible community use.
- `moderate`: some stars/forks or clear external adoption, but still early.
- `early`: low adoption but plausible, with clear docs and recent activity.
- `experimental`: 0-star / 0-fork or otherwise unvalidated; include only when the concept is useful enough to watch.

After the table, add:

- **Top picks**: 2-4 repos the user should act on first.
- **Decision notes**: what appears installable, what needs credentials, what is only a reference, and what should be inspected before any install decision.
- **Method**: date range, source types, and proxy metrics.

## Guardrails

- Do not recommend suspicious repos that mimic paid products, bypass licensing, or look like credential/activation abuse.
- Do not pad the list with coding-only tools.
- Do not claim "trending" from memory; use current GitHub or web data.
- Do not treat stars alone as relevance, but do treat 0 stars / 0 forks as a serious lack of validation.
- Do not place unvalidated 0-star repos above validated alternatives unless you explicitly explain the exception.
- Clearly distinguish an installable Codex skill from a standalone app.
- Never install, clone, download, run setup commands, or change local skill/plugin files as part of the radar output. Only report candidates and wait for the user's explicit install decision.
