# tinnitus-help-automation

Generator repo for Tinnitus Help content. Holds the n8n workflow JSON snapshots
(`new_post.json`, `share_post.json`, `share_sound.json`, `publish_reel.json`,
`publish_facebook_video.json`, `share_video*.json`), `content-database.json`,
`post_guidelines.md`, and generated MDX under `content/`.

The site repo (`~/Coding/tinnitus-blog`) is the source of truth for anything
shipped — generated MDX is copied there and edited there.

## The publish-content skill is NOT in this repo

`publish-content` covers **both** Tinnitus Help and Crypto Wiki from a single
copy, versioned in the other automation repo:

    ~/Coding/crypto-wiki-automation/.claude/skills/publish-content/

`~/.claude/skills/publish-content` is a symlink into that path, which is how
Claude Code discovers it — so it works from any directory, including this one.

This is deliberate. The publish sequence is identical for both sites; only the
n8n workflow IDs and the per-site formatting rules differ, and those are already
data inside the skill (`scripts/quality_gate.py` has a `SITES` dict and infers
the site from the MDX path). Two copies would drift.

Edits to the skill, and the `.n8n-api-key` / `.pexels-api-key` secrets and
`.n8n-backups/` it depends on, all live in `crypto-wiki-automation`.

**Exception:** this repo owns its own committed workflow JSON. When a live n8n
fix to a Tinnitus workflow is important or major, sync it back into the matching
file here and commit — see the "Persisting workflow fixes" section in the skill.
