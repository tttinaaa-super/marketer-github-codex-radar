#!/usr/bin/env python3
"""Rank GitHub repos for marketer usefulness inside Codex.

Input can be either a GitHub search API payload with an "items" array or a
plain JSON array of repository objects.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CATEGORIES = {
    "insights": ("research", "trend", "scraper", "search", "analytics", "audience", "social listening"),
    "decks": ("presentation", "powerpoint", "ppt", "pptx", "slides", "deck"),
    "creative": ("creative", "design", "image", "poster", "ad creative", "thumbnail", "generative"),
    "social": ("social", "instagram", "tiktok", "youtube", "rednote", "xiaohongshu", "xhs", "publisher"),
    "video": ("video", "shorts", "reels", "ugc", "motion", "storyboard"),
    "brand": ("brand", "logo", "identity", "brand kit", "guideline", "visual system"),
    "automation": ("workflow", "automation", "agent", "n8n", "pipeline", "scheduler"),
    "knowledge": ("rag", "knowledge", "docs", "document", "pdf", "notion", "wiki"),
}

CODING_ONLY = (
    "compiler",
    "framework",
    "sdk",
    "debugger",
    "kubernetes",
    "database driver",
    "orm",
    "lint",
    "benchmark",
    "leetcode",
)

CODEX_FIT_INSTALL = ("skill.md", "codex", "claude code", "openclaw", "mcp", "agent skill", "skills/")
CODEX_FIT_WRAP = ("cli", "desktop app", "api", "docker", "npm", "pip", "command line")


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def days_since(value: str | None, now: datetime) -> float:
    parsed = parse_time(value)
    if parsed is None:
        return 365.0
    return max((now - parsed).total_seconds() / 86400.0, 0.0)


def text_for(repo: dict[str, Any]) -> str:
    parts = [
        repo.get("name"),
        repo.get("full_name"),
        repo.get("description"),
        " ".join(repo.get("topics") or []),
        repo.get("readme_excerpt"),
    ]
    return " ".join(str(part) for part in parts if part).lower()


def category_scores(text: str) -> dict[str, int]:
    scores: dict[str, int] = {}
    for category, keywords in CATEGORIES.items():
        score = sum(1 for keyword in keywords if keyword in text)
        if score:
            scores[category] = score
    return scores


def codex_fit(text: str, repo: dict[str, Any]) -> str:
    if repo.get("has_skill_md") or any(token in text for token in CODEX_FIT_INSTALL):
        return "install"
    if any(token in text for token in CODEX_FIT_WRAP):
        return "wrap"
    if category_scores(text):
        return "reference"
    return "skip"


@dataclass
class Row:
    repo: str
    url: str
    use: str
    fit: str
    validation: str
    stars: int
    forks: int
    updated_days: float
    score: float
    why: str


def validation_label(stars: int, forks: int, repo: dict[str, Any]) -> str:
    if stars >= 100 or forks >= 25:
        return "strong"
    if stars >= 20 or forks >= 5:
        return "moderate"
    if stars > 0 or forks > 0:
        return "early"
    return "experimental"


def score_repo(repo: dict[str, Any], now: datetime) -> Row | None:
    if repo.get("archived") or repo.get("disabled"):
        return None

    text = text_for(repo)
    categories = category_scores(text)
    coding_penalty = sum(1 for keyword in CODING_ONLY if keyword in text)
    if not categories or coding_penalty >= 2:
        return None

    stars = int(repo.get("stargazers_count") or 0)
    forks = int(repo.get("forks_count") or repo.get("fork_count") or 0)
    updated_days = min(days_since(repo.get("pushed_at") or repo.get("updated_at"), now), 365.0)
    freshness = max(0.0, 30.0 - updated_days) / 30.0
    adoption = math.log10(stars + 1) * 18.0 + math.log10(forks + 1) * 10.0
    relevance = sum(categories.values()) * 7.0
    fit = codex_fit(text, repo)
    fit_bonus = {"install": 18.0, "wrap": 10.0, "reference": 4.0, "skip": -20.0}[fit]
    validation = validation_label(stars, forks, repo)
    validation_penalty = {"strong": 0.0, "moderate": 0.0, "early": 8.0, "experimental": 28.0}[validation]
    score = relevance + adoption + freshness * 10.0 + fit_bonus - coding_penalty * 8.0 - validation_penalty

    ordered_categories = sorted(categories, key=lambda item: categories[item], reverse=True)
    use = ", ".join(ordered_categories[:2])
    why = repo.get("description") or "Relevant active GitHub project."

    return Row(
        repo=repo.get("full_name") or repo.get("name") or "unknown",
        url=repo.get("html_url") or "",
        use=use,
        fit=fit,
        validation=validation,
        stars=stars,
        forks=forks,
        updated_days=updated_days,
        score=score,
        why=why,
    )


def load_payload(path: Path | None) -> list[dict[str, Any]]:
    data = json.loads(path.read_text() if path else sys.stdin.read())
    if isinstance(data, dict) and isinstance(data.get("items"), list):
        return data["items"]
    if isinstance(data, list):
        return data
    raise SystemExit("expected a JSON array or GitHub search payload with items[]")


def render(rows: list[Row]) -> str:
    out = [
        "| Rank | Repository | Use | Codex fit | Validation | Stars | Forks | Updated | Why it matters |",
        "| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for rank, row in enumerate(rows, 1):
        repo = f"[{row.repo}]({row.url})" if row.url else row.repo
        out.append(
            f"| {rank} | {repo} | {row.use} | {row.fit} | {row.validation} | "
            f"{row.stars} | {row.forks} | {row.updated_days:.1f}d | {row.why} |"
        )
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path)
    parser.add_argument("--limit", type=int, default=12)
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    rows = [row for row in (score_repo(repo, now) for repo in load_payload(args.input)) if row]
    rows.sort(key=lambda row: row.score, reverse=True)
    print(render(rows[: args.limit]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
