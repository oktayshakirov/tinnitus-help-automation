# Handoff: reactive-tinnitus

Cloud session ran Steps 1-3 of `publish-content-tinnitus`. Steps 4-6 need your
Mac. Delete this file before merging PR #2.

Session: https://claude.ai/code/session_0141tvHn4L4skmaxcxS93rDp
Branch: `claude/confident-ritchie-yvokfc` (PR #2, draft)

## What is done

- `content/posts/reactive-tinnitus.mdx` written by hand (n8n was unreachable).
  `quality_gate.py` passes 29/29, 0 fails 0 warns: 1,703 words, 15 internal
  links, `sources:` (4), `faq:` (5), `medical:` default true, description
  129 chars, no dashes or curly quotes.
- Slug registered in `content-database.json` (`blog.reactive-tinnitus`).
- Main `<Image>` alt text set from the photo you chose.

## What is NOT done

1. `/images/reactive-tinnitus.jpg` does not exist. Nothing downloaded.
2. Nothing staged into `tinnitus-blog`.
3. Nothing pushed to production, so no deploy gate, no notification.
4. Share Post workflow not run.
5. `next_orders` in `content-database.json` left at `{"blog": 35}` - unclear
   whether the New Post workflow increments it. Check and bump if it should.
6. Source URLs not re-curled. All four are URLs already live in the archive
   (NIDCD tinnitus x8, NHS tinnitus x5, AAO-HNS guideline x4, NIDCD
   noise-induced hearing loss x1), so they were verified when those posts
   shipped, but this session could not confirm them - nidcd.nih.gov, nhs.uk
   and entnet.org are all 403'd by the cloud network policy.

## Why the cloud session stopped

- n8n: `localhost:5678` returned `000` on `/healthz` and `/api/v1/workflows`.
  Not running, and not reachable from a cloud container regardless.
- Pexels: `www.pexels.com`, `images.pexels.com` and `api.pexels.com` all got
  `403 to CONNECT` from the agent proxy. No `.pexels-api-key` on the box
  (it lives in `crypto-wiki-automation`, which is not cloned here).
- No image tooling: no `sips`, no `cwebp`, no PIL.
- `tinnitus-blog` is not cloned here at all.

## Pick up here

### 1. Pull both repos

    cd ~/Coding/tinnitus-help-automation
    git pull --autostash origin claude/confident-ritchie-yvokfc
    cd ~/Coding/tinnitus-blog && git pull --autostash

### 2. Fetch the main image

You chose Pexels photo `13755910`
(https://www.pexels.com/photo/a-woman-with-freckles-on-her-face-looking-afar-13755910/).

    KEY=$(cat ~/Coding/crypto-wiki-automation/.pexels-api-key)
    curl -s -H "Authorization: $KEY" \
      https://api.pexels.com/v1/photos/13755910 | python3 -m json.tool

Take `.src.original`, then:

    curl -sL "<src.original>?w=1600" -o /tmp/reactive-raw.jpg
    sips -Z 800 /tmp/reactive-raw.jpg \
      --out ~/Coding/tinnitus-blog/public/images/reactive-tinnitus.jpg
    ls -lh ~/Coding/tinnitus-blog/public/images/reactive-tinnitus.jpg

Confirm under 200 KB. Then dup-check it against the archive - `ahash` and
`archive_hashes` in
`.claude/skills/publish-content-tinnitus/scripts/pick_main_image.py` are
importable for a one-off check. Pexels re-serves its popular stock, so this
matters even for a hand-picked photo.

### 3. Check the alt text against the real photo

`content/posts/reactive-tinnitus.mdx` line 37 currently reads:

    alt="Woman with freckles on her face looking into the distance, listening
    warily for a sound she expects to rise."

That was written from the Pexels title, not from looking at the image. Open the
downloaded file and fix it if it describes something that is not there.

### 4. Stage and re-gate

    cp content/posts/reactive-tinnitus.mdx ~/Coding/tinnitus-blog/content/posts/
    python3 .claude/skills/publish-content-tinnitus/scripts/quality_gate.py \
      ~/Coding/tinnitus-blog/content/posts/reactive-tinnitus.mdx

With the real archive present this should pass without the `--archive`
override the cloud session needed. Review in the dev server.

### 5. Push (needs your go)

Commit the post AND the image together in `tinnitus-blog`. Check
`git status` for the untracked image - a missing image ships a broken page.

Then the deploy gate, both must return 200 before anything is shared:

    curl -sL -o /dev/null -w '%{http_code}\n' https://www.tinnitushelp.me/blog/reactive-tinnitus
    curl -sL -o /dev/null -w '%{http_code}\n' https://www.tinnitushelp.me/images/reactive-tinnitus.jpg

A `000` is a bad host, not a slow deploy. Note the path is `/blog/`, though
the MDX lives in `content/posts/`.

Step 5b is automatic - `.github/workflows/notify-new-content.yml` fires on the
push and syncs to Firestore. Confirm the run went green in the Actions tab.

### 6. Share (needs your go, posts publicly)

Pre-flight: confirm `images/posts/reactive-tinnitus.png` does NOT exist in
this automation repo. It did not as of this handoff. The Upload node is
create-only and fails with "sha wasn't supplied" if a previous run left one
behind - `git rm` and push first if so.

Start n8n, then run Share Post `jtUStrxCt23FGNDk` with
`formData: { slug: "reactive-tinnitus" }`.

If you trigger the Form Trigger by hand rather than through MCP: it must be
`multipart/form-data` (`curl -F`), and fields are named `field-0`, `field-1`
by index, NOT by label. `-F "slug=..."` returns HTTP 200 and emits
`slug: null`. Confirm the trigger node's output actually carries the slug.

Verify: every node succeeded; the Telegram result has a `photo` array nested
at `result.photo` (not top level); Facebook and Instagram outputs each carry
an `id`; download the run's APITemplate `download_url_png` and look at it to
confirm the banner rendered with title and photo and no black spot.

## Worth doing while you are in here

Only 8 of 81 posts carry `sources:`/`faq:`. `ototoxic-medications-and-tinnitus`
has neither and also has curly quotes, despite discussing chemotherapy and
dosing - that is the YMYL failure the 2026-08-25 audit flagged, still live.
`hyperacusis-and-tinnitus` is the same. Backfilling those two is probably worth
more than the next new post.
