# Query Playbook

Use this reference when the GitHub candidate pool is noisy or sparse.

## Candidate Searches

Start with a 7-day `pushed:>` cutoff:

```text
presentation AI pushed:>YYYY-MM-DD
content creation AI pushed:>YYYY-MM-DD
creative AI design agent pushed:>YYYY-MM-DD
marketing automation AI pushed:>YYYY-MM-DD
social media AI publisher pushed:>YYYY-MM-DD
SKILL.md Codex marketing presentation pushed:>YYYY-MM-DD
agent skills creative marketing pushed:>YYYY-MM-DD
```

If too narrow, remove one constraint:

```text
AI agents pushed:>YYYY-MM-DD
AI design creative brand pushed:>YYYY-MM-DD
AI automation research content workflow pushed:>YYYY-MM-DD
```

## What To Inspect

For finalists, inspect:

- README or repo description.
- Topics and recent push date.
- Root files and whether `SKILL.md`, `skills/`, `.codex-plugin/`, or CLI docs exist.
- Required credentials, especially paid APIs.
- Safety and legitimacy: avoid repos that appear to bypass paid services or collect credentials.

## Marketer Fit Categories

- `insights`: trend research, audience research, scraping, social listening, analytics.
- `decks`: PowerPoint, slides, editable PPTX, pitch or report creation.
- `creative`: ad creative, imagery, posters, campaign visuals, thumbnails.
- `social`: Instagram, TikTok, YouTube, Xiaohongshu/RedNote, publishing workflows.
- `video`: UGC ads, shorts, reels, storyboards, product videos.
- `brand`: logo, brand kit, identity, design guide, visual consistency.
- `automation`: repeatable workflows, n8n, agents, publishing pipelines.
- `knowledge`: RAG, document libraries, internal knowledge bases.

## Codex Fit Labels

- `install`: Codex can directly use it as a skill/plugin/MCP/CLI with clear setup.
- `wrap`: useful app/CLI, but needs a custom skill or wrapper to make Codex operate it smoothly.
- `reference`: useful idea or manual tool, but not worth installing in Codex yet.
- `skip`: coding-only, suspicious, stale, or too weak for marketer use.

## Reporting Pattern

Lead with the practical shortlist, not a raw dump of repositories. Include a short method note:

```text
Method: searched GitHub repositories updated from DATE to DATE; ranked by marketer relevance, installability in Codex, adoption proxies (stars/forks), and recency. Exact weekly star deltas were unavailable, so I used these proxies.
```
