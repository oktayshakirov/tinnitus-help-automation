# tinnitus-help-automation

Generator repo for Tinnitus Help content. Holds the n8n workflow JSON snapshots
(`new_post.json`, `share_post.json`, `share_sound.json`, `publish_reel.json`,
`publish_facebook_video.json`, `share_video*.json`), `content-database.json`,
`post_guidelines.md`, and generated MDX under `content/`.

The site repo (`~/Coding/tinnitus-blog`) is the source of truth for anything
shipped — generated MDX is copied there and edited there.

## publish-content-tinnitus

The publishing skill lives here, at `.claude/skills/publish-content-tinnitus/`
(`~/.claude/skills/publish-content-tinnitus` symlinks to it). It covers
tinnitushelp.me only.

**As of 2026-08-25 this is a standalone copy, not shared with Crypto Wiki.**
Originally one `publish-content` skill covered both sites (living in
`crypto-wiki-automation`, branching per-site inside `quality_gate.py`), on the
reasoning that the sequence was identical and two copies would drift. Split on
request into `publish-content-tinnitus` here and `publish-content-crypto` in
`crypto-wiki-automation`, to let the two diverge independently as the sites'
needs change. **A fix made in one does not apply to the other — check both
skills when changing a rule that might be shared** (e.g. the deploy-gate
polling logic, the Pexels dup-check flow).

Shared n8n instance/secrets still live in `crypto-wiki-automation`
(`.n8n-api-key`, `.pexels-api-key`, `.n8n-backups/`) — see the skill's
Prerequisites section. This repo owns its own committed workflow JSON
snapshots; sync important live n8n fixes back into them per the skill's
"Persisting workflow fixes" section.
