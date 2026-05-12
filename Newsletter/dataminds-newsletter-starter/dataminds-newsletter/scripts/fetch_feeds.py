"""
Fetch recent articles from all feeds in feeds.yaml.
Outputs output/candidates.json with one entry per article.

Usage:
    python scripts/fetch_feeds.py --days 60
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse

try:
    import feedparser  # type: ignore
    import yaml  # type: ignore
except ImportError:
    print("Missing dependencies. Run: pip install feedparser pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
FEEDS_FILE = ROOT / "feeds.yaml"
OUTPUT_FILE = ROOT / "output" / "candidates.json"


def parse_date(entry) -> datetime | None:
    """Extract published date from a feedparser entry. Returns UTC datetime or None."""
    for field in ("published_parsed", "updated_parsed", "created_parsed"):
        ts = entry.get(field)
        if ts:
            return datetime(*ts[:6], tzinfo=timezone.utc)
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=60, help="Lookback window in days")
    args = ap.parse_args()

    config = yaml.safe_load(FEEDS_FILE.read_text())
    feeds = config["feeds"]
    excludes = set(config.get("exclude_domains", []))

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    print(f"Fetching {len(feeds)} feeds, filtering to last {args.days} days "
          f"(since {cutoff.date()})", file=sys.stderr)

    candidates: list[dict] = []
    for feed in feeds:
        try:
            parsed = feedparser.parse(feed["url"])
        except Exception as e:
            print(f"  ✗ {feed['name']}: {e}", file=sys.stderr)
            continue

        kept = 0
        for entry in parsed.entries:
            published = parse_date(entry)
            if published is None or published < cutoff:
                continue

            url = entry.get("link", "")
            domain = urlparse(url).netloc.lower()
            if any(domain.endswith(d) for d in excludes):
                continue

            candidates.append({
                "source": feed["name"],
                "category": feed.get("category", "general"),
                "title": entry.get("title", "").strip(),
                "author": (entry.get("author")
                           or entry.get("dc_creator")
                           or "Unknown"),
                "url": url,
                "published": published.isoformat(),
                "summary": (entry.get("summary", "") or "")[:500].strip(),
            })
            kept += 1
        print(f"  ✓ {feed['name']}: {kept}", file=sys.stderr)

    # Newest first.
    candidates.sort(key=lambda c: c["published"], reverse=True)

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(candidates, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nTotal: {len(candidates)} candidates -> {OUTPUT_FILE}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
