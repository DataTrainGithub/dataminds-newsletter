"""
Substitute WordPress media ID placeholders in the generated shortcode.

After running the newsletter generator you'll have:
    output/post-with-placeholders.txt   — contains {{News_AI_Copilot}} etc.
    output/images/News_AI_Copilot.png ... — one image per unique category

Manual step in wp-admin:
    1. Go to Media > Add New
    2. Drag-and-drop all category images from output/images/News_*.png
    3. For each uploaded image, the ID is in the URL when you click it
       (e.g. wp-admin/upload.php?item=2810 -> ID is 2810)
    4. Note each ID — you need one per unique category image

Then run:
    python scripts/finalize.py

The script prompts for the ID of each category image and writes
output/post-<month>-<year>.txt (e.g. output/post-may-2026.txt) — ready to
paste into a new WordPress post via the Backend Editor (Code tab).

Tip: enable "Show IDs in Media Library" by adding this snippet to your
theme's functions.php (one-time, optional):

    add_filter('manage_media_columns', function($cols) {
        $cols['media_id'] = 'ID';
        return $cols;
    });
    add_action('manage_media_custom_column', function($col, $id) {
        if ($col === 'media_id') echo $id;
    }, 10, 2);
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "output" / "post-with-placeholders.txt"

# Known category placeholders and their WordPress media IDs.
# If a placeholder is not listed here, the script prompts for it.
DEFAULT_MEDIA_IDS = {
    "News_AI_Copilot": "2798",
    "News_DAX": "2800",
    "News_Data_Engineering": "2799",
    "News_Microsoft_Fabric": "2801",
    "News_Power_BI": "2802",
    "News_Real_Time_Intelligence": "2803",
    # "News_SQL_Server": "",  # upload image and add ID here when first used
}


def _month_slug() -> str:
    """Derive month slug from the post title line, e.g. 'may-2026'."""
    try:
        text = INPUT.read_text(encoding="utf-8")
        # Anchor to the newsletter title to avoid matching month names in article bodies.
        m = re.search(
            r"dataMinds News Round up.*?"
            r"(January|February|March|April|May|June|July|August|"
            r"September|October|November|December)\s+(\d{4})",
            text, re.DOTALL | re.IGNORECASE,
        )
        if m:
            return f"{m.group(1).lower()}-{m.group(2)}"
    except Exception:
        pass
    from datetime import date
    slug = date.today().strftime("%B-%Y").lower()
    print(f"WARNING: could not find month in post title; using today's date: {slug}", file=sys.stderr)
    return slug


def main() -> int:
    if not INPUT.exists():
        sys.exit(f"Not found: {INPUT}\nRun the generator first.")

    slug = _month_slug()
    OUTPUT = ROOT / "output" / f"post-{slug}.txt"

    content = INPUT.read_text(encoding="utf-8")

    # Find unique {{News_*}} placeholders in document order (preserving first-seen order).
    all_found = re.findall(r"\{\{(News_[A-Za-z_]+)\}\}", content)
    seen: set[str] = set()
    unique_placeholders: list[str] = []
    for p in all_found:
        if p not in seen:
            seen.add(p)
            unique_placeholders.append(p)

    n = len(unique_placeholders)
    if n == 0:
        sys.exit("No {{News_*}} placeholders found in the input file.")

    print(f"Found {n} unique category image(s) to fill in:")
    for p in unique_placeholders:
        print(f"  {{{{{p}}}}}  ({p}.png)")
    print()

    media_ids: dict[str, str] = {}
    for placeholder in unique_placeholders:
        if placeholder in DEFAULT_MEDIA_IDS:
            media_ids[placeholder] = DEFAULT_MEDIA_IDS[placeholder]
            print(
                f"Using saved media ID for {placeholder}.png: "
                f"{media_ids[placeholder]}"
            )
            continue

        raw = input(f"WordPress media ID for {placeholder}.png: ").strip()
        if not raw.isdigit():
            sys.exit(f"Expected an integer ID, got: {raw!r}")
        media_ids[placeholder] = raw

    for placeholder, media_id in media_ids.items():
        content = content.replace(f"{{{{{placeholder}}}}}", media_id)

    OUTPUT.write_text(content, encoding="utf-8")
    print(f"\n✓ Wrote {OUTPUT}")
    print(f"  Copy the contents of that file into a new WordPress post")
    print(f"  via wp-admin -> Posts -> Add New -> Backend Editor -> Code tab.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
