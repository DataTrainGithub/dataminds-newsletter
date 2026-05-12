---
name: newsletter
description: Generate the monthly dataMinds newsletter — fetch candidates, present interactive picklist, summarise selected articles, generate category images, collect WordPress media IDs, and produce ready-to-paste shortcode
---

Generate the monthly dataMinds newsletter. Follow every step in order. Pause and wait for user input where indicated — do not proceed past a user-input step until you have their answer.

---

## Step 1 — Lookback period

Ask the user: **"How many days back should we look for articles? (default: 60)"**

Use their answer as `<DAYS>`. If they press Enter or say "default", use 60.

---

## Step 2 — Fetch candidates

Run:
```
python scripts/fetch_feeds.py --days <DAYS>
```

Read `output/candidates.json`. It contains one object per article with fields: `source`, `title`, `author`, `url`, `published`, `summary`, `category`.

---

## Step 3 — Editorial filter and propose picks

Apply the dataMinds editorial criteria:

**Include:**
- Practical use cases, implementation walkthroughs, governance pieces
- Independent analyses of Microsoft data platform features
- Community voices (consultants, MVPs, practitioners) on Fabric, Power BI, SQL, Azure data, AI agents
- Major event recaps (community write-ups only — not the keynote itself)

**Exclude:**
- Microsoft-published feature announcements (already filtered by excluded_domains, but double-check)
- Vendor marketing disguised as tutorials
- Generic "what is X" intro pieces for total beginners
- Anything duplicating a topic already well represented in the shortlist

**Variety target:** across picks, aim for a mix of categories. Don't fill the list with 10 articles on the same theme even if they are all good.

From the filtered candidates, propose **15–20 picks**. Present them as a numbered list, grouped loosely by topic for readability:

```
 1. "Article Title" — Author (Source) — DD Mon YYYY
    WHY: one sentence explaining why this fits the newsletter

 2. "Article Title" — Author (Source) — DD Mon YYYY
    WHY: ...
```

After the list ask:
> **"Reply with the numbers you want to include (e.g. `1,3,5-8,12`). Aim for 8–12 articles. You can also add a URL not in the list with `add:<url>`."**

---

## Step 4 — Confirm selection

Echo the selected titles as a numbered list. Ask:
> **"Confirm this selection? (yes / or tell me what to change)"**

Apply any requested changes and re-confirm before continuing.

---

## Step 5 — Fetch full articles and write summaries

For each confirmed article, in order:

1. Use `web_fetch` to retrieve the full article text.
2. Write a summary following the voice in `examples/voice.md`. Rules:
   - **80–130 words of body text only** — no preamble, no author prefix line
   - Start directly with: **"[Author's full name] [strong action verb]..."**
     - Do NOT start with `In "<strong>Title</strong>",`
     - Do NOT start with "This article..."
     - Never write "the author" — always use the person's name
   - End with a punchy editorial verdict in `<strong>...</strong>` tags
   - **No em dashes (—)**. Use comma, colon, semicolon, or parentheses instead
   - British/Flemish spelling is fine ("centre", "favour")
3. Assign exactly one category from this canonical list:
   - `AI & Copilot`
   - `DAX`
   - `Data Engineering`
   - `Microsoft Fabric`
   - `Power BI`
   - `Real-Time Intelligence`
   - `SQL Server`

---

## Step 6 — Sort by category

Sort all confirmed articles **alphabetically by category**. Within the same category, keep the original selection order.

---

## Step 7 — Generate images for new categories

The known categories that already have saved WordPress media IDs are:

| Slug | Category |
|------|----------|
| `News_AI_Copilot` | AI & Copilot |
| `News_DAX` | DAX |
| `News_Data_Engineering` | Data Engineering |
| `News_Microsoft_Fabric` | Microsoft Fabric |
| `News_Power_BI` | Power BI |
| `News_Real_Time_Intelligence` | Real-Time Intelligence |
| `News_SQL_Server` | SQL Server |

For each **unique category** used in this edition:

1. Compute its slug: replace ` & ` with `_`, spaces with `_`, hyphens with `_`, then prepend `News_`.
2. If the slug is **not** in the table above, run:
   ```
   python scripts/generate_image.py --category "<category label>"
   ```
   The image is saved to `output/images/<slug>.png`.

After running, tell the user which new images were created and instruct them:
> "Please upload these new category images to WordPress (Media > Add New), note each image's ID (visible in the URL as `?item=XXXX`), and come back here."

---

## Step 8 — Collect WordPress media IDs

For each unique category used in this edition, ask the user for the media ID. Handle these two cases:

**Known category** — show the current saved ID and allow override:
> "Saved media ID for `News_AI_Copilot` (`AI & Copilot`) is **2798**. Press Enter to keep it, or type a new ID."

**New category** — ask for the ID after upload:
> "What media ID did WordPress assign to `<slug>.png`?"

After collecting all IDs:
- If any IDs are new (not previously in `scripts/finalize.py` DEFAULT_MEDIA_IDS), update `scripts/finalize.py` by adding the new slug → ID pairs to the `DEFAULT_MEDIA_IDS` dictionary, so future runs remember them.

---

## Step 9 — Render the shortcode

Construct the WPBakery shortcode exactly as follows.

### URL encoding rule
Replace only `https://` with `https%3A//` (encode the colon after the protocol). Leave all other characters in the URL as-is.

### File structure

**`output/post-with-placeholders.txt`** — use `{{News_SlugName}}` placeholders instead of real media IDs. This is the editable source of truth.

**`output/post-<month>-<year>.txt`** — same content with real media IDs substituted (e.g. `output/post-june-2026.txt`). This is the file to paste into WordPress.

### Shortcode template

```
[us_separator size="large"]
[vc_row css=".vc_custom_1633617659553{margin-top: -50px !important;margin-bottom: -50px !important;}"][vc_column width="2/3"]
[vc_column_text]<h3>TITLE</h3>
<p>SUMMARY_TEXT</p>
<p>Author: AUTHOR_NAME</p>[/vc_column_text]
[us_btn label="Read more" link="url:ENCODED_URL|title:Read%20more|target:%20_blank|"]
[us_separator size="small"]
[/vc_column][vc_column width="1/3" offset="vc_hidden-xs"]
[us_image image="MEDIA_ID_OR_PLACEHOLDER" size="medium" align="right" style="shadow-2" onclick="custom_link" link="url:ENCODED_URL||target:%20_blank|" animate="afr" animate_delay="1"]
[/vc_column][/vc_row]
```

Rules:
- The `[us_separator size="large"]` appears **once at the very top** of the file (before the first article). It does NOT repeat between articles.
- Between articles use `[us_separator size="small"]` (already inside each article block above).
- `Author:` line has **no `<strong>` tags** — plain text only.
- `SUMMARY_TEXT` is the body text only — no author prefix, no title preamble.
- In `post-with-placeholders.txt`, use `{{News_AI_Copilot}}` etc. as the image value.
- In `post-<month>-<year>.txt`, substitute the real media ID integer.

Save both files to `output/`.

Also save a `output/summaries.json` with the article data for future reference:
```json
[
  {
    "title": "...",
    "author": "...",
    "url": "...",
    "category": "...",
    "summary": "..."
  }
]
```

---

## Step 10 — Hand off to Lou

Print this summary:

> **Newsletter ready!**
>
> **Files generated:**
> - `output/post-<month>-<year>.txt` — paste into WordPress Backend Editor (Code tab)
> - `output/post-with-placeholders.txt` — editable source of truth for future tweaks
>
> **To publish:**
> 1. Go to wp-admin → Posts → Add New
> 2. Switch to Backend Editor → Code tab
> 3. Paste the contents of `output/post-<month>-<year>.txt`
> 4. Set the post title, featured image, and tags as usual
>
> **New category images generated** (if any):
> - `output/images/<slug>.png` — already uploaded, IDs saved

Then output the full shortcode in a code block so Lou can also copy it directly from the conversation without opening the file.
