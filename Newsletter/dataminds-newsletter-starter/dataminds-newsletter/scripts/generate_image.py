"""
Generate a category label image for the dataMinds newsletter.

Each image is a solid #E82E00 background with the technology category
written in white, centred. No external API or network call required.

Usage:
    python scripts/generate_image.py --category "Microsoft Fabric"

Output is saved to output/images/News_<slug>.png automatically.
You can override with --output if needed.

--seed is accepted but ignored (kept for CLI compatibility).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Missing dependency. Run: pip install pillow", file=sys.stderr)
    sys.exit(1)

BG_COLOR = "#E82E00"
TEXT_COLOR = "white"
WIDTH = 1024
HEIGHT = 1024
FONT_SIZE = 96

ROOT = Path(__file__).resolve().parent.parent


def category_to_slug(category: str) -> str:
    """Convert a category label to a News_ filename stem.

    "AI & Copilot"          -> "News_AI_Copilot"
    "Real-Time Intelligence" -> "News_Real_Time_Intelligence"
    "Data Engineering"       -> "News_Data_Engineering"
    """
    slug = category.replace(" & ", "_").replace(" ", "_").replace("-", "_")
    return f"News_{slug}"


def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "calibrib.ttf", "Calibri Bold.ttf",
        "arialbd.ttf", "Arial Bold.ttf",
        "DejaVuSans-Bold.ttf",
    ]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    print("WARNING: no TrueType font found; text will render at small default size", file=sys.stderr)
    return ImageFont.load_default()


def generate(category: str, output: Path) -> None:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font = _load_font(FONT_SIZE)

    # Word-wrap long categories so they fit within 80 % of the width.
    words = category.split()
    lines: list[str] = []
    current = ""
    max_px = WIDTH * 0.80
    for word in words:
        test = (current + " " + word).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_px:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)

    line_height = FONT_SIZE * 1.25
    total_h = line_height * len(lines)
    y = (HEIGHT - total_h) / 2

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        x = (WIDTH - (bbox[2] - bbox[0])) / 2
        draw.text((x, y), line, fill=TEXT_COLOR, font=font)
        y += line_height

    output.parent.mkdir(parents=True, exist_ok=True)
    img.save(output)
    print(f"Saved {output}", file=sys.stderr)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--category", help="Technology category label")
    ap.add_argument(
        "--output", type=Path, default=None,
        help="Output path. Defaults to output/images/News_<slug>.png",
    )
    ap.add_argument("--seed", type=int, default=42, help="Ignored, kept for compatibility")
    # Legacy --prompt alias so old callers don't break.
    ap.add_argument("--prompt", dest="category", help=argparse.SUPPRESS)
    args = ap.parse_args()
    if not args.category:
        ap.error("--category (or legacy --prompt) is required")

    output = args.output or ROOT / "output" / "images" / f"{category_to_slug(args.category)}.png"
    generate(args.category, output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
