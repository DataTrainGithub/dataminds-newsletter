# dataMinds Newsletter — Agent Instructions

You are helping Lou Segers produce the monthly dataMinds newsletter, published
on https://dataminds.be. Each edition is a round-up of ~10 community blog
posts about Microsoft Fabric, AI use cases on Microsoft tech, and SQL.

## Editorial criteria

**Include:**
- Practical use cases, implementation walkthroughs, governance pieces
- Independent analyses of Microsoft data platform features
- Community voices (consultants, MVPs, practitioners) writing about Fabric,
  Power BI, SQL, Azure data, AI agents
- Major event recaps (Microsoft Ignite, FabCon, Microsoft Build) — but only
  community write-ups, not the keynote itself

**Exclude:**
- Microsoft-published feature release announcements
- Vendor marketing posts disguised as tutorials
- Generic "what is Fabric" intro pieces aimed at total beginners
- Anything older than 60 days from the target publish date

**Variety target:** across the 10 picks, aim for a mix of topics. Don't end
up with 10 articles about MCP servers even if they're all good.

## Workflow

When the user says "generate the [month] edition" or similar:

1. **Discover** — run `python scripts/fetch_feeds.py --days 60` to pull recent
   posts from all sources in `feeds.yaml`. Output is `output/candidates.json`.

2. **Curate** — read the candidates, propose 10–12 picks to the user with a
   one-line rationale each. Wait for approval or edits before continuing.

3. **Summarise** — for each approved pick, `web_fetch` the full article and
   write a summary in the established voice (see `examples/voice.md`). Save
   to `output/summaries.json`.
   **Never use em dashes (—) or long dashes in summaries or titles.** Use a
   short hyphen (-), comma, semicolon, colon, or parentheses instead. Apply
   this rule while writing, not as a post-processing step.

4. **Assign category labels and sort** — assign each article a category label:
   "AI & Copilot", "DAX", "Data Engineering", "Microsoft Fabric", "Power BI",
   "Real-Time Intelligence", or "SQL Server". Then **sort articles alphabetically
   by category** before proceeding. Articles in the same category keep their
   original relative order.

5. **Generate images** — collect the unique category labels across all articles,
   then for each unique category call:
   ```
   python scripts/generate_image.py --category "<label>"
   ```
   Output is auto-named `output/images/News_<slug>.png` (e.g. `News_AI_Copilot.png`).
   Articles sharing a category reuse the same image file and the same
   placeholder in the post. The script produces a solid #E82E00 background
   with the category in white. No API key or network call needed.

6. **Render template** — use `examples/template.txt` (Jinja2) to assemble the
   final WPBakery shortcode. The template emits `{{IMG_1}}` ... `{{IMG_10}}`
   placeholders where media IDs will go. Save to
   `output/post-with-placeholders.txt`.

7. **Hand off to Lou** — print a clear summary:
   > "Generated N images in `output/images/` and shortcode in
   > `output/post-with-placeholders.txt`. To get the final WordPress code:
   > 1. Upload all N images from `output/images/` to wp-admin → Media → Add New
   > 2. Note the N media IDs in upload order (visible in the URL: `?item=XXXX`)
   > 3. Run `python scripts/finalize.py` and paste the IDs when prompted
   > 4. The final file is saved as `output/post-<month>-<year>.txt`
   >    (e.g. `output/post-may-2026.txt`) — copy its contents into
   >    wp-admin → Posts → Add New → Backend Editor → Code tab"

## Summary voice

Strict pattern, derived from past editions:

```
Author: [Full Author Name]

In "<strong>[Article Title]</strong>", [Author Name] [action verb]. [What it
covers in 1-2 sentences]. [A specific concrete detail that hints at the depth
— a named tool, technique, or finding.] [One-line closing assessment.]
```

- 80-130 words per summary
- Closer line is a punchy editorial verdict, not a generic summary
- Don't say "the author" - always use the person's name
- Don't start with "This article..."
- No em dashes (--). Use a comma, colon, semicolon, or parentheses instead

See `examples/voice.md` for worked examples from the April edition.

## Image style

Each image is a solid **#E82E00** background with the technology category
written in white, centred. Generated locally with Pillow — no AI, no network.

Pass `--category` with the label (e.g. `--category "Microsoft Fabric"`).
The `--prompt` alias still works for backwards compatibility.

Valid category labels: "Microsoft Fabric", "Power BI", "DAX", "SQL Server",
"Azure AI", "Real-Time Intelligence", "Data Engineering", "AI & Copilot".

## File map

- `feeds.yaml` — curated RSS sources. Edit to add/remove blogs.
- `examples/voice.md` — voice-and-tone reference with worked summaries.
- `examples/template.txt` — Jinja2 template for the WPBakery shortcode.
- `scripts/fetch_feeds.py` — RSS aggregator.
- `scripts/generate_image.py` — category label image generator (Pillow, local).
- `scripts/finalize.py` — interactive media ID substitution.
- `output/` — generated artifacts (candidates, summaries, images, post).

## Constraints

- Never invent quotes or facts about an article. Only state what's in the post.
- Never use Microsoft's own announcement blogs as sources.
- If an article's full text can't be fetched, flag it to Lou and ask whether
  to substitute.
- The newsletter is published roughly mid-month. Default to "previous full
  month" for picks unless told otherwise.
- No API keys or paid services are involved in this workflow.
