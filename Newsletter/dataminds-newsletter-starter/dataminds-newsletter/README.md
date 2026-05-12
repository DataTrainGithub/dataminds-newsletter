# dataMinds Newsletter Generator

Monthly automation for the dataMinds.be news round-up post. No API keys
required. No paid services. The only manual step is bulk-uploading a small
number of category images via wp-admin Media Library (~30 seconds).

## First-time setup

1. **Install Python dependencies**
   ```bash
   pip install feedparser pyyaml requests jinja2 pillow
   ```

2. **(Optional but helpful) Show media IDs in WP Media Library**

   By default, the Media Library doesn't show IDs in the list view. To
   make step 4 of the monthly run easier, add this snippet to your theme's
   `functions.php` once:
   ```php
   add_filter('manage_media_columns', function($cols) {
       $cols['media_id'] = 'ID';
       return $cols;
   });
   add_action('manage_media_custom_column', function($col, $id) {
       if ($col === 'media_id') echo $id;
   }, 10, 2);
   ```
   Without this snippet, the IDs are still visible: click any image and
   look at the URL — `wp-admin/upload.php?item=2810` means ID 2810.

3. **Verify the feed list works**
   ```bash
   python scripts/fetch_feeds.py --days 60
   head output/candidates.json
   ```
   You should see 50-150 articles. Edit `feeds.yaml` to add/remove sources.

4. **Test image generation**
   ```bash
   python scripts/generate_image.py --category "Microsoft Fabric"
   ```
   Open `output/images/News_Microsoft_Fabric.png`. You should see a solid
   #E82E00 background with "Microsoft Fabric" in white. One image is
   generated per unique category; articles sharing a category reuse it.

## Monthly run

In the project folder:
```bash
claude
```

Then say:
> *"Generate the May 2026 edition."*

Claude Code will:
1. Run `fetch_feeds.py` and load `output/candidates.json`
2. Propose 10-12 candidates with rationale - you approve or edit
3. Fetch each article and write a summary in the established voice
4. Assign a category label to each article and sort alphabetically
5. Generate one image per unique category into `output/images/News_<Category>.png`
6. Render the shortcode with `{{News_<Category>}}` placeholders into
   `output/post-with-placeholders.txt`

Then you take over for ~5 minutes:

7. **Bulk-upload images** in wp-admin - Media - Add New. Drag all
   `News_*.png` files from `output/images/` at once.

8. **Note the media IDs**, one per uploaded file. If you added the snippet
   in step 2, they're in the list view directly. Otherwise click each
   upload and read the ID from the URL.

9. **Finalize**
   ```bash
   python scripts/finalize.py
   ```
   Enter one ID per category image when prompted. The script writes
   `output/post-<month>-<year>.txt` (e.g. `output/post-may-2026.txt`).

10. **Create the post** in wp-admin: Posts - Add New - switch to the
    Backend Editor "Code" tab - paste the contents of
    `output/post-<month>-<year>.txt` - set the date, title, and publish.

Total time: ~10 minutes including review.

## Files

- `CLAUDE.md` - agent instructions (source of truth for behaviour)
- `feeds.yaml` - curated RSS sources
- `examples/voice.md` - voice-and-tone reference with worked summaries
- `examples/template.txt` - Jinja2 template for the WPBakery shortcode
- `scripts/fetch_feeds.py` - RSS aggregator
- `scripts/generate_image.py` - category label image generator (Pillow, local, no network)
- `scripts/finalize.py` - interactive media ID substitution

## Iteration

If a summary doesn't sound right: edit `examples/voice.md` to sharpen the
voice. It improves every month.

If candidates miss good blogs: add them to `feeds.yaml`.

If WordPress rejects the shortcode: edit `examples/template.txt`.
