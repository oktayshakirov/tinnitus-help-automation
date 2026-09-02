---
name: publish-content-tinnitus
description: Publish content to tinnitushelp.me via the local n8n workflows - suggest topics, generate the article, quality-gate it, stage locally for review, then push (deploy-gated) and share to social media. Use when the user wants to create/publish/share a Tinnitus Help post. For thecrypto.wiki use publish-content-crypto instead.
---

# Publish Content — Tinnitus Help

Full agent loop: **suggest topics → user picks → generate via n8n → quality gate → stage locally → fetch main-image candidates (user picks) → user reviews → push (deploy gate) → share → verify.**

This skill covers **tinnitushelp.me only**. For thecrypto.wiki, use `publish-content-crypto` in `crypto-wiki-automation` — it is a separate copy, not a shared script, so a fix here does not apply there automatically.

**Repo paths (absolute; this skill works from any directory):** automation repo `/Users/oktayshakirov/Coding/tinnitus-help-automation`; site (production) repo `/Users/oktayshakirov/Coding/tinnitus-blog`. The `.n8n-api-key` and `.n8n-backups/` for the *crypto* workflows live in `crypto-wiki-automation`, but the Tinnitus workflow JSON snapshots (`new_post.json`, `share_post.json`, `share_sound.json`, `publish_reel.json`, `publish_facebook_video.json`) live here.

**Production URLs (do NOT guess these - a wrong host returns curl `000` forever and looks exactly like a slow deploy):**

| Domain | Article URL | Main image URL |
|---|---|---|
| `https://www.tinnitushelp.me` | `/blog/<slug>` (note: **`/blog/`**, though the MDX lives in `content/posts/`) | `/images/<slug>.jpg` |

301s to `www`, so always `curl -L`. A `000` status is DNS/connection failure, not a pending deploy - re-check the host before continuing to poll; 10 minutes were once burned polling a `tinnitus-help.com` that does not exist while the page was already live at `www.tinnitushelp.me`.

**Where this skill lives / cross-device:** the real files are versioned in the `tinnitus-help-automation` repo at `.claude/skills/publish-content-tinnitus/`; `~/.claude/skills/publish-content-tinnitus` is a **symlink** into it, which is how Claude Code discovers the skill. So edits to `SKILL.md` or `scripts/` are committed like any repo change (backup workflow JSON to the crypto repo's `.n8n-backups/` still applies for workflow edits, since that's where n8n API access and backups live - see Prerequisites). **To set up a new device:** clone `tinnitus-help-automation` AND `crypto-wiki-automation` (the second one holds the shared n8n secrets), then `ln -s <tinnitus-help-automation>/.claude/skills/publish-content-tinnitus ~/.claude/skills/publish-content-tinnitus`, and recreate the two gitignored secrets locally in `crypto-wiki-automation` (`.n8n-api-key`, `.pexels-api-key`).

## Prerequisites
- **n8n must be running** at `http://localhost:5678` (user starts it manually with `n8n`; it is NOT always on). If unreachable, ask the user to start it.
- Prefer the `mcp__n8n-local__*` MCP tools. If they're not loaded in this session, call the MCP endpoint directly with curl: POST `http://127.0.0.1:5678/mcp-server/http` (JSON-RPC `tools/call`), auth `Authorization: Bearer <token>` - read the token from the `n8n-local` server entry in `~/.claude.json`. Poll executions via REST: `http://127.0.0.1:5678/api/v1/executions/<id>?includeData=true` with header `X-N8N-API-KEY` from the gitignored `/Users/oktayshakirov/Coding/crypto-wiki-automation/.n8n-api-key` (shared n8n instance - the key isn't per-site).
- **Triggering a Form Trigger without the MCP tools** (reading the MCP bearer token out of `~/.claude.json` may be blocked by the permission classifier): fetch the workflow over REST, read the form trigger's `webhookId`, and POST to `http://127.0.0.1:5678/form/<webhookId>`. Two non-obvious requirements, both of which fail *quietly*:
  - It must be **`multipart/form-data`** (`curl -F`, not `--data-urlencode`). Form-encoded returns HTTP 500 `Workflow could not be started!`, and the real reason (`Expected multipart/form-data`) only shows up in the execution record.
  - Fields are named **`field-0`, `field-1`, ... by index**, NOT by field label. `-F "topic=..."` returns **HTTP 200** and the trigger emits `topic: null`; the AI then invents an unrelated topic and the run looks completely normal. **Always confirm the Form Trigger node's output actually carries your topic/slug before trusting a run.**
- **Polling gotcha:** `GET /api/v1/executions` **excludes running executions by default**, so right after a trigger the newest entry is the previous run - easy to misread as "my run failed." Use `?status=running` to find the new id, then poll `/executions/<id>` directly.
- `git pull` both relevant repos first: `tinnitus-help-automation` and `tinnitus-blog`. Use `git pull --autostash` - the automation repo often carries uncommitted skill edits, which make a plain rebase pull abort.
- **Main-image fetch (Step 4)** needs a free Pexels key at `crypto-wiki-automation/.pexels-api-key` (gitignored - shared across both sites, lives in the crypto repo). If missing, ask the user to create it from `https://www.pexels.com/api/`. Only `sips` + `cwebp` are available locally (no ImageMagick); `sips` does the resize/JPEG re-encode.
- Workflow-edit gotcha: the n8n public-API PUT rejects `settings.binaryMode`; filter `settings` to allowed keys (executionOrder, callerPolicy, availableInMCP, ...) or the PUT 400s.

## Workflow registry (Form Triggers; run with `inputs: {type:"form", formData:{...}}`)
| Action | Workflow ID | formData |
|---|---|---|
| New Post | `pddxBAmv2k2nSBv2` | `{ topic }` |
| Share Post | `jtUStrxCt23FGNDk` | `{ slug }` |
| Share Sound | `UcubZDb1sKnszcZX` | `{ slug }` |
| Publish Reel | `1GTSF6izfwA1gpig` | `{ videoUrl, coverUrl, caption, durationSeconds }` |
| Publish Facebook Video | `Lyhn5U7pYhrAs9x7` | `{ videoUrl, title, description, thumbUrl }` |

**Publish Reel** is driven by the `publish-video` skill, not by this one. It posts one
vertical video as an Instagram Reel and a Facebook Reel; `videoUrl` and `coverUrl` must
be publicly reachable for the length of the run (the skill opens a cloudflared quick
tunnel over the render folder). Facebook Reels accepts 3 to 90 seconds only, which is
why `durationSeconds` is required and checked before anything uploads.

**Publish Facebook Video** posts a long-form video natively to the Page feed - not a
Reel, no duration cap, `POST /me/videos` with `file_url` rather than the three-phase
Reels upload. Built 2026-08-20 to test whether native video earns more organic reach
than posting a YouTube link. **It replaced the Share Video workflow**, which posted a
YouTube URL to Facebook and Telegram and let them unfurl it into a card. It was deleted
on 2026-08-20 - a link post sends the viewer to YouTube and earns the reach an outbound
link earns, which is the thing native upload exists to avoid. The last JSON is in the
crypto repo's `.n8n-backups/*.before-delete.json` - **local only**, since
`.n8n-backups/` is gitignored, so that safety net does not survive a fresh clone. Pulls
`title`/`description` straight from `youtube-audit video <id>` rather than writing
Facebook-native copy, since the source videos are already public on YouTube. This is a
straight clone of the crypto version with the TinnitusHelp Page credential swapped in -
check that node before running, since a wrong credential posts to the wrong brand and
cannot be undone quietly.

**Pass the full YouTube description; the workflow trims it.** `Normalise Input` keeps
the first paragraph and the line carrying the article link, and drops the rest - the
second summary, the chapter list, and the repeat of the same URL at the bottom. A whole
YouTube description under a Facebook video buries the one line a reader acts on and
prints the URL twice. The trim lives in the workflow rather than at the caller so it
cannot be forgotten. It carries the link's own line **verbatim** rather than
relabelling it: an article video says `Full article: <url>`, a sound session says
`More at <url>` and has no article behind it, so a hardcoded "Full article" label
would be a lie there.

**If the source folder has no thumbnails, pull each video's `maxresdefault.jpg` from
YouTube** rather than rendering new ones - that is the poster already live on the
channel, so the Facebook cover matches. **Match files to YouTube videos by duration,
not by title**: the filenames drift from the published titles, and duration matched
all five tinnitus videos within a second on 2026-08-20.

**The `FB Reel Upload` node posts to `rupload.facebook.com`, not `graph.facebook.com`.**
Meta documents its auth as an `Authorization: OAuth <token>` header; the node instead
uses the existing Facebook Graph credential as a *predefined credential type*, which
n8n injects as `?access_token=` on the query string. **Verified working on 2026-08-20** -
rupload accepts the query string as well as the header, so no Header Auth credential is
needed. If it ever starts 401ing, that is the first thing to suspect and a Header Auth
credential (`Authorization` = `OAuth <page token>`) on that one node is the fix.

## Step 1 - Suggest 10 topics
Read `content-database.json` in `tinnitus-help-automation` (`blog`/`zen`). Gap-analyze vs existing titles; use WebSearch for trends. Present 10 options with a one-line "why" each. **The chosen topic becomes title AND slug verbatim - keep it short.**

## Step 2 - Generate
Execute the New Post workflow. GPT-5 takes 1-3 min (retryOnFail 3x is set); if the run still fails with ECONNRESET/ETIMEDOUT, just re-run. On success it commits the MDX + updates `content-database.json` in the automation repo.

## Step 3 - Quality gate (pull the automation repo, check the MDX)
**Run the automated gate first:** `python3 scripts/quality_gate.py <path-to.mdx>` (script dir is this skill's folder). It checks all of the below deterministically and exits non-zero on any hard FAIL - fix those, re-run, then eyeball anything a script can't judge (image relevance, factual/date accuracy, link *aptness*).

It resolves the DB + image archive itself. Override with `--db` / `--archive`.

Known non-issues it deliberately tolerates: markdown table separator rows (`| --- |`) are stripped before the dash check, `#anchor`/`?query` links validate against the base page, and link targets are checked against the DB **union the MDX actually on disk** (the DB has drifted and is missing at least two live posts).

Checks: 1,200-2,500 words; 8-15 internal links, **bold** `**[Text](/path)**`, each page linked at most once, all slugs valid vs DB; exactly 2 `<Image />` and the **first one is the main image**; body images **not repeated in posts published close together** - reusing an archive image across the site is fine and expected; what matters is that someone reading a few recent posts back to back never sees the same picture twice. The gate warns when a body image also appears in any of the 5 most recent other posts by frontmatter date (`--recent-window`); the Build node keeps reaching for the same few files, and `audiologist.jpg` ended up as the body image on three consecutive posts. On a warning, swap in a different archive file, or fetch a new one with `pick_main_image.py` and add it under a generic reusable name (e.g. `sound-therapy-headphones.jpg`, `patient-consultation.jpg`) rather than a slug-specific one - old images are free to come back around later; exactly 2-3 lowercase tags from the fixed vocab; description 120-135 chars (hard max 140, the site truncates); **`sources:` (3-5, authoritative) and `faq:` (4-5) present** - see Step 3b, this is the part that most affects post quality; no em/en dashes or `--` (plain `-` only); **no curly quotes** (`'`/`'`/`"`/`"` -> straight; applies to body AND the frontmatter description); no trailing metadata JSON (fenced or bare); ads never adjacent to images; no `## References` heading in the body (the `sources:` block replaces it).

Most violations are auto-fixed by the Build node now - if one slips through, fix the article AND add a deterministic fix to the workflow node + `post_guidelines.md` (backup to the crypto repo's `.n8n-backups/` first; mutate the workflow dict in place; PUT only `name,nodes,connections,settings`).
**Persisting workflow fixes:** live n8n edits only survive in the gitignored `.n8n-backups/`. When a fix is **important/major** (fixes a broken workflow, changes a contract, or prevents a defect on every future run), also sync the live workflow into this repo's committed JSON snapshot (`new_post.json`, `share_post.json`, `share_sound.json`, ...) and commit, so it survives an n8n reset - minor tweaks can stay live-only. Known deterministic fixes already committed: `slugToTitle` Title-Cases spaced-lowercase topics and splits on spaces-or-hyphens (was returning lowercase titles verbatim); the Build node moves a headless intro (prose between the main `<Image>` and the first `## <Highlighter>`) down under that heading, so every post opens with a headline.

**Answer-first opening.** The first paragraph under the first heading must *directly answer the question the title implies*, in roughly the first 40-60 words, before any throat-clearing. "Does X cause tinnitus?" opens with "Yes/No/Sometimes, because..."; a "best X" or "X vs Y" topic opens by naming the top pick(s) and who each suits. This is the sentence Google lifts into a featured snippet and ChatGPT/Gemini quote in an answer - burying it costs the citation. The `<Blockquote>` above it stays a scene-setting hook; the answer goes in the body paragraph. For question and comparison posts, also add a heading that matches the exact search phrase (`## <Highlighter>What is the best tinnitus app?</Highlighter>`), and for a roundup, one sub-section per specific variant people actually search (`### Best tinnitus masking app`, `### Best white noise app for tinnitus`).

Post conventions: opens `<Blockquote>` → main `<Image>` → **first `## <Highlighter>` heading** (the intro/hook paragraphs go *under* that heading - a post that opens with a bare paragraph before any heading is a FAIL; the Build node now moves such prose under the first heading automatically); `## <Highlighter>Heading</Highlighter>`; `<AdComponent />`; first body image = main image (`/images/{slug}.jpg` flat); standalone sub-group labels that head a bullet list use `##### ` (h5); posts carry no `author` field. Title is auto-derived from the slug (Title Cased, small words lowercased, acronyms preserved via a map in the Build node) - the AI does not write it; spot-check any new acronym (add it to the `acronyms` map in the Build node if it comes out wrong, e.g. `cbt`/`tmj`/`airpods`).

## Step 3b - The three frontmatter blocks that carry E-E-A-T

**This is the highest-value part of a tinnitus post and the part the workflow
does not write on its own.** Tinnitus is YMYL (Your Money Your Life) health
content: Google holds it to a higher quality bar than an ordinary blog, and the
site was built with the machinery to meet that bar. An audit on 2026-08-25 found
the pipeline had stopped feeding it - every post generated in 2026 carried none
of the three, while the older hand-written posts (`what-is-tinnitus`,
`tinnitus-and-sleep`, `pulsatile-tinnitus`, `ototoxic-medications`) carried all
of them. The worst case was `serotonin-and-tinnitus`, which discussed SSRI
start-up spikes, tapering and dose titration, said "some studies suggest" four
times, and cited nothing.

### `sources:` - REQUIRED on any post making a health claim

Renders as a real `References` list at the foot of the post
(`src/components/References/`). Its own docstring is the reason: outbound links
to primary sources are an E-E-A-T signal on YMYL topics, so they are rendered as
normal followed links.

```yaml
sources:
  - title: 'Tinnitus - treatment and coping'
    url: 'https://www.nidcd.nih.gov/health/tinnitus'
    publisher: 'NIDCD, National Institutes of Health'
```

- **3-5 sources.** `title`, `url`, and `publisher` on every entry.
- **Primary and authoritative only.** The domains already established across the
  archive, in rough order of use: `nidcd.nih.gov`, `entnet.org` (AAO-HNS
  clinical practice guidelines), `ata.org` (American Tinnitus Association),
  `nhs.uk`, `who.int`, `mayoclinic.org`, `cochrane.org`, `ncbi.nlm.nih.gov`.
  Never another blog, never a supplement retailer, never a content farm. The
  gate warns on any domain outside that set - widen it deliberately, not by
  reflex.
- **Verify every URL resolves before committing.**
  `curl -sL -o /dev/null -w '%{http_code}'`. The AI invents plausible deep links
  (a real case on the crypto side: two nonexistent app-store URLs). A 404 in a
  reference list is worse than no reference list - it is a broken authority
  signal on the exact page that needs one.
- **The source must actually support the claim.** Do not staple a generic NIDCD
  tinnitus overview onto a post about magnesium and call it cited. If the
  specific claim has no authoritative source behind it, soften the claim
  instead.
- **This does NOT mean a `## References` heading in the body.** That is still a
  hard FAIL - it is what the AI writes when left alone, and it duplicates the
  component. The structured frontmatter block is the only correct form.

### `faq:` - REQUIRED, 4-5 entries

Renders a visible `FaqSection` and feeds `faqSchema()` (FAQPage JSON-LD) from
`BlogPost.SEO.tsx`. Same shape as the crypto side's `faqs`, but the key here is
singular `faq`.

```yaml
faq:
  - question: 'Why is my tinnitus worse at night?'
    answer: 'Your bedroom is the quietest environment you spend time in, so ...'
```

- Write the questions as **real search queries** - the phrasing someone types or
  says, not a heading rewritten with a question mark. `tinnitus-and-sleep` is
  the model to copy.
- Answers 40-90 words, self-contained, plain text (the JSON-LD takes the plain
  answer, so no markdown links inside).
- **Be honest about the payoff.** Google restricted FAQ *rich results* in 2023 to
  well-known authoritative government and health sites, so do not expect the
  snippet. The value here is the on-page content: it targets long-tail question
  queries and People Also Ask directly, which is where this site actually wins.

### `medical:` - set `false` on culture and history posts

Defaults to **true**, which types the page as `MedicalWebPage` and renders
`<MedicalDisclaimer />`. Correct for health posts; wrong and slightly absurd on
an art-history piece. The seven posts that set `medical: false` are
`celebrities-with-tinnitus`, `did-van-gogh-have-tinnitus`, `tinnitus-in-art`,
`tinnitus-in-history`, `tinnitus-in-digital-age`, `tinnitus-in-wildlife`,
`what-tinnitus-teaches-us` - the tell is tags like `history`, `society`, or a
topic about tinnitus in culture rather than tinnitus in a body. On those posts
`sources:` is optional (cite where a historical claim needs it); on every
medical post it is mandatory.

## Step 4 - Stage locally + pick the main image
Copy the MDX to `tinnitus-blog/content/posts/` - do NOT commit.

**Main image, auto-fetched from Pexels.**
1. Derive a concrete visual search query from the topic (avoid brand-heavy/ad-like results). **Aim for an editorial, aesthetically strong photo, not a clinical or literal one** - the user has said explicitly they want the blog to look good rather than "medicine and ugly". Before writing the query, `Read` 2-3 recent main images from the site archive to calibrate: the house style is dramatic low-key portraits, bold coloured studio backdrops, and clean minimal shots of people - not equipment, otoscopes, or clip-art. Query words that reliably land it: `dramatic light`, `low key`, `chiaroscuro`, `side profile`, `black background`, `neon studio portrait`. A conceptual tie beats a literal one (a rim-lit side profile where the light catches the ear reads better than a doctor holding an otoscope).
   Add a demographic word when the topic is adult-facing (`adult`, `mature man`, `woman`) - a bare query like `person covering ear` returns almost entirely children and teenagers.
2. Run `scripts/pick_main_image.py --query "<query>" --slug <slug> --out <scratchpad>/imgpick --archive tinnitus-blog/public/images [--width 800]` (script dir is this skill's folder; default width 800). It downloads candidates, resizes to the standard width, re-encodes JPEG < 200 KB, and prints a JSON manifest (file path, KB, photographer, Pexels URL).
   **Always pass `--archive`.** Pexels re-serves its popular stock constantly, so candidates are frequently a photo already published under another slug - the script aHashes each candidate against the archive, drops anything within `--dup-threshold` (default 6), backfills a replacement, and reports what it rejected on stderr. This is not theoretical: the ear close-up returned for `human ear close up macro skin` is byte-identical to the existing `earwax-and-tinnitus.jpg`.
3. `open` the `candidate_*.jpg` AND send them with `SendUserFile` (`display: "render"`) so they appear inline in chat, then ask which to use. Offer a re-roll (`--page 2`, or a new `--query`); expect to need 2-3 rounds before one lands, and vary the *direction* between rounds rather than just re-running the same query.
4. On pick, copy the chosen candidate to `tinnitus-blog/public/images/<slug>.jpg` and delete the preview dirs. **Then rewrite the main `<Image>` alt text to describe the photo actually chosen** - the AI writes alt text blind against an imagined image, so it will otherwise describe something that is not on the page.

   If the user supplies a specific Pexels photo URL instead of picking a candidate, pull it by id via `GET https://api.pexels.com/v1/photos/<id>` (auth header is the bare key), download `src.original` with `?w=1600`, then `sips -Z 800` + JPEG re-encode. Still dup-check it against the archive - `pick_main_image.ahash` / `archive_hashes` are importable for exactly this. Pexels needs no attribution, but the manifest keeps the photographer/URL if the user ever wants to credit.

Site standard: posts ~800px wide JPG. The script already keeps every candidate < 200 KB.

Then let the user review (offer dev server). Fold their feedback into `post_guidelines.md`/the workflow so the next run is right by default.

## Step 5 - Push (only on explicit approval)
Commit post + ALL new images (check `git status` for untracked images - a missing image ships a broken page) to `tinnitus-blog`, push. Then **DEPLOY GATE**: poll the production article URL AND main-image URL until both return 200, using the exact hosts + path shapes from the **Production URLs** table at the top of this skill (`curl -sL`). If the first poll returns `000`, stop and fix the URL - that is a bad host, not a slow deploy. Never share before this passes - the banner generator fetches the main image from production (black-spot banner otherwise).

### Step 5b - Push notification (automatic)
**Nothing to run.** The push to main triggers `.github/workflows/notify-new-content.yml`, which waits for the deployment to go live and then syncs to Firestore, which sends the notification. Check the repo's Actions tab to confirm the run went green - it takes a few minutes because it waits on the deploy.

If the run failed or timed out, re-run it from the Actions tab, or send it by hand from the site repo with `npm run sync-content`. Never move the sync into `npm run build` - it used to live there, which is exactly why taps in the first ~15s hit a 404.

## Step 6 - Share (only on explicit approval - posts publicly)
Before running: confirm the share image doesn't already exist in this automation repo (`images/posts/<slug>.png` via GitHub API; if present from a previous run, `git rm` + push first - the Upload node is create-only and fails with "sha wasn't supplied").
Run the matching Share workflow. It posts to Telegram (binary upload), Instagram + Facebook (Twitter nodes are intentionally disconnected - no X API). Verify: every node success; Telegram result has a `photo` array (**nested at `result.photo`, not top-level** - checking the top level looks like a failure on a perfectly good run); Facebook/Instagram outputs each carry an `id`; download the run's APITemplate `download_url_png` and view it to confirm the banner rendered (title + photo, no black spot).
**Single-channel re-share**: temporarily remove the other channel targets from `Format Social Post`'s connections, run, then restore.

## Safety
- Never push or share without the user's explicit go for that step.
- Secrets: `.n8n-api-key` (REST) and `.pexels-api-key` (Step 4 images) live in `crypto-wiki-automation` (shared instance/account, not per-site), and the MCP bearer token (in `~/.claude.json`) - never commit or echo them.
- Workflow edits: backup JSON to the crypto repo's `.n8n-backups/` first; verify the PUT response.
