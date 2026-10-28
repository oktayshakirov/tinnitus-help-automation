# Tinnitus Help Automation

The content pipeline behind [tinnitushelp.me](https://tinnitushelp.me), a blog
of evidence-based articles and sound-therapy resources for people living with
tinnitus: topic research, article writing, an automated quality gate,
publishing and social distribution.

The articles are written by an AI agent working through a
[Claude Code](https://claude.com/claude-code) skill, checked by a scripted
quality gate, reviewed by a human, and then deployed and shared by
[n8n](https://n8n.io) workflows. Medical claims are sourced and checked against
their sources before anything is staged.

## The pipeline

1. **Suggest.** The agent reads `content-database.json` (every published post)
   and proposes topics that fill real gaps.
2. **Write.** One article per run, following `post_guidelines.md`, with sourced
   claims, internal links and an answer-first opening.
3. **Quality gate.** `quality_gate.py` checks length, internal links against
   the database, body images from the real archive and not repeated in recent
   posts, ad and image placement, and typography before anything is staged.
4. **Stage and review.** The article is staged in the site repo and reviewed
   locally. Main images come from Pexels via `pick_main_image.py`.
5. **Publish.** A push to the site repo, then a deploy gate that waits until the
   page is actually live before anything is shared.
6. **Share.** n8n workflows render a social card and post it to X, Facebook,
   Instagram and Telegram.

## What is here

| Path | Contents |
|---|---|
| `.claude/skills/publish-content-tinnitus/` | The agent skill: the full run, the quality gate and the image picker |
| `post_guidelines.md` | House style and structure for posts |
| `content-database.json` | The index of everything published, used for topic gaps and link validation |
| `content/`, `images/` | Generated articles and images, before they are copied into the site repo |
| `*.json` (root) | Committed snapshots of the n8n workflows |

### n8n workflows

| Workflow | What it does |
|---|---|
| `share_post`, `share_sound` | Render a social card (APITemplate.io) and post to X, Facebook, Instagram and Telegram |
| `share_video`, `share_video_telegram` | Announce a new video on Facebook and Telegram |
| `publish_reel`, `publish_facebook_video` | Publish a finished vertical video as an Instagram/Facebook Reel, or long-form video natively on Facebook |
| `new_post` | The original OpenAI-based generator, kept as a fallback |

Credentials are referenced by n8n id only; no keys or tokens are stored in this
repo.

## Setup

This pipeline shares one n8n instance with
[crypto-wiki-automation](https://github.com/oktayshakirov/crypto-wiki-automation),
which holds the n8n and Pexels API keys. It expects that repo and the site repo
(`tinnitus-blog/`) to be checked out next to this one.

The videos for the site come from
[video-edit-automation](https://github.com/oktayshakirov/video-edit-automation).

## Author

Oktay Shakirov
