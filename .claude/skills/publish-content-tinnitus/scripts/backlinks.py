#!/usr/bin/env python3
"""Find (and optionally add) missing internal links across the site.

For every article, look for the first plain-prose mention of another page
(an OG, an exchange, or a post concept from link_aliases.json) that the
article does not link yet, and propose wrapping it as **[text](/path)**.

    backlinks.py --site ~/Coding/crypto-wiki                 # report everything
    backlinks.py --site ... --target /crypto-ogs/jeff-yan    # who should link to a new page
    backlinks.py --site ... --apply [--kinds og,exchange]    # write the links

Rules it follows (same as the quality gate and the guideline docs):
- one link per target per article, never a self-link
- only in paragraph/list prose: never in headings, quotes, tables, images,
  components, inside an existing link, or inside **bold**
- never a second link in a sentence that already has one
- stops adding once the article reaches --max-links internal links (15)
- OGs and exchanges first, then post concepts
- on posts, a linked OG/exchange is also appended to the frontmatter
  `crypto-ogs:` / `exchanges:` list (the gate requires the two to match)
- 'review' aliases (words with a second meaning, like Gemini) are reported but
  never applied

It does not touch `updated`. Adding links is not a content revision, and
bumping dateModified on dozens of pages for that would be noise.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DIRS = (("crypto-ogs", "og"), ("exchanges", "exchange"), ("posts", "post"))
URL_PREFIX = {}                                 # set from the alias file's url_prefix
ORDER = {"og": 0, "exchange": 1, "post": 2}
FM_FIELD = {"og": "crypto-ogs", "exchange": "exchanges"}
COUNT_RE = re.compile(r"\[[^\]]+\]\((/[^)]+)\)")   # same count as quality_gate.py
LINK_RE = re.compile(r"\]\((/[a-z0-9-]+/[^)#?\s]+)")       # any internal page link
MASK_RES = [
    re.compile(r"!\[[^\]]*\]\([^)]*\)"),      # images
    re.compile(r"\[[^\]]*\]\([^)]*\)"),       # links
    re.compile(r"\*\*.+?\*\*"),               # bold spans
    re.compile(r"`[^`]*`"),                   # inline code
    re.compile(r"https?://\S+"),              # bare urls
]


def split_fm(txt):
    m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
    return (m.group(1), txt[m.end():], m.end()) if m else ("", txt, 0)


def fm_value(fm, key):
    m = re.search(r'^%s:\s*["\']?(.*?)["\']?\s*$' % re.escape(key), fm, re.M)
    return m.group(1) if m else None


def load_entities(site, aliases):
    ents = []
    for d, kind in DIRS:
        folder = os.path.join(site, "content", d)
        if not os.path.isdir(folder):
            continue                          # e.g. tinnitushelp.me has posts only
        for f in sorted(os.listdir(folder)):
            if not f.endswith(".mdx") or f.startswith("_"):
                continue
            path = f"{aliases.get('url_prefix', {}).get(d, '/' + d)}/{f[:-4]}"
            fm, _, _ = split_fm(open(os.path.join(folder, f)).read())
            title = fm_value(fm, "title") or ""
            if fm_value(fm, "draft") == "true":
                continue
            a = aliases.get(path)
            if kind == "post" and not a:
                continue                      # question titles never appear in prose
            phrases = (a or {}).get("phrases") or [title]
            ents.append({
                "path": path, "kind": kind, "title": title,
                "phrases": sorted(phrases, key=len, reverse=True),
                "ci": (a or {}).get("ci", aliases.get("default_ci", False)),
                "review": (a or {}).get("review", False),
                "nfb": (a or {}).get("not_followed_by",
                                     []) + aliases.get("default_not_followed_by", []),
                "npb": (a or {}).get("not_preceded_by", []),
                "skip": set((a or {}).get("skip_files", [])),
            })
    ents.sort(key=lambda e: ORDER[e["kind"]])
    return ents


def masked(line):
    spans = []
    for r in MASK_RES:
        spans += [m.span() for m in r.finditer(line)]
    return spans


def eligible_lines(body):
    """Yield (index, line) for paragraph and list-item prose only."""
    fence = jsx = False
    for i, line in enumerate(body.split("\n")):
        s = line.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if jsx:                               # inside a multi-line <Component ...>
            if s.endswith(("/>", ">")) or s.startswith(("</", "/>")):
                jsx = False
            continue
        if s.startswith("<") and not s.endswith(">"):
            jsx = True
            continue
        if fence or not s:
            continue
        if re.match(r"^[A-Za-z_]+=", s) or s[0] in "{}":   # stray JSX props
            continue
        if s[0] in "#>|!<" or s.startswith(("import ", "export ")):
            continue
        yield i, line


def sentence_bounds(line, pos):
    start = max(line.rfind(". ", 0, pos), line.rfind("? ", 0, pos),
                line.rfind("! ", 0, pos))
    start = 0 if start < 0 else start + 2
    ends = [e for e in (line.find(". ", pos), line.find("? ", pos),
                        line.find("! ", pos)) if e >= 0]
    return start, (min(ends) + 1 if ends else len(line))


def find_mention(lines, ent):
    flags = re.I if ent["ci"] else 0
    for i, line in lines:
        spans = masked(line)
        for ph in ent["phrases"]:
            for m in re.finditer(r"(?<![\w./-])%s(?![\w-]|\.\w)" % re.escape(ph),
                                 line, flags):
                a, b = m.span()
                if any(s <= a < e or s < b <= e for s, e in spans):
                    continue
                after = line[b:].lstrip(" ")
                if any(re.match(re.escape(w) + r"(?!\w)", after) for w in ent["nfb"]):
                    continue
                before = line[:a].rstrip(" ").split(" ")[-1] if a else ""
                if before in ent["npb"]:
                    continue
                ss, se = sentence_bounds(line, a)
                if "](/" in line[ss:se] or "](http" in line[ss:se]:
                    continue
                return i, a, b, m.group(0)
    return None


def plan_file(fp, kind, ents, max_links, kinds, approve=False):
    txt = open(fp).read()
    fm, body, _ = split_fm(txt)
    d = os.path.basename(os.path.dirname(fp))
    self_path = f"{URL_PREFIX.get(d, '/' + d)}/{os.path.basename(fp)[:-4]}"
    linked = set(LINK_RE.findall(body))
    count = sum(1 for u in COUNT_RE.findall(body) if not u.startswith("/images/"))
    lines = list(eligible_lines(body))
    body_lines = body.split("\n")
    out = []
    for ent in ents:
        if ent["path"] == self_path or ent["path"] in linked:
            continue
        if os.path.basename(fp)[:-4] in ent["skip"]:
            continue                          # a reviewed false positive
        hit = find_mention(lines, ent)
        if not hit:
            continue
        i, a, b, text = hit
        line = body_lines[i]
        ctx = line[max(0, a - 60):b + 60].replace("\n", " ")
        item = {"target": ent["path"], "kind": ent["kind"], "title": ent["title"],
                "text": text, "line": i, "a": a, "b": b, "ctx": ctx,
                "review": ent["review"], "capped": count >= max_links}
        out.append(item)
        item["apply"] = ((approve or not ent["review"]) and not item["capped"]
                         and ent["kind"] in kinds)
        if item["apply"]:
            count += 1
            # keep later matches from landing in the same sentence
            new = line[:a] + f"**[{text}]({ent['path']})**" + line[b:]
            body_lines[i] = new
            lines = [(j, body_lines[j] if j == i else l) for j, l in lines]
            linked.add(ent["path"])
    return fm, "\n".join(body_lines), out


def add_fm(fm, field, title):
    m = re.search(r"^%s:\s*\[(.*?)\]\s*$" % re.escape(field), fm, re.M)
    if m:
        items = [x.strip() for x in m.group(1).split(",") if x.strip()]
        if f'"{title}"' in items:
            return fm
        items.append(f'"{title}"')
        return fm[:m.start()] + f"{field}: [{', '.join(items)}]" + fm[m.end():]
    anchor = re.search(r"^(authors?|draft):", fm, re.M)
    line = f'{field}: ["{title}"]\n'
    return fm[:anchor.start()] + line + fm[anchor.start():] if anchor else fm + "\n" + line.rstrip()


def sync_fm(fm, body, titles):
    """Every OG/exchange a post links in its body belongs in its frontmatter list."""
    added = []
    for path in dict.fromkeys(LINK_RE.findall(body)):
        for field, prefix in (("crypto-ogs", "/crypto-ogs/"), ("exchanges", "/exchanges/")):
            if path.startswith(prefix) and path in titles:
                new = add_fm(fm, field, titles[path])
                if new != fm:
                    added.append(titles[path]); fm = new
    return fm, added


def apply(fp, kind, fm, new_body, items, titles):
    todo = [x for x in items if x["apply"]]
    added = []
    if kind == "post":
        fm, added = sync_fm(fm, new_body, titles)
    open(fp, "w").write(f"---\n{fm}\n---\n" + new_body)
    return len(todo), added


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default=os.path.expanduser(
        os.environ.get("BACKLINKS_SITE", "~/Coding/tinnitus-blog")))
    ap.add_argument("--aliases", default=os.path.join(HERE, "link_aliases.json"))
    ap.add_argument("--target", help="only report/apply links to this path, e.g. /crypto-ogs/jeff-yan")
    ap.add_argument("--files", nargs="*", help="limit to these article files")
    ap.add_argument("--kinds", default="og,exchange,post", help="target kinds to apply")
    ap.add_argument("--max-links", type=int, default=15)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--approve-review", action="store_true",
                    help="also apply review-only aliases (use with --target/--files after reading the matches)")
    a = ap.parse_args()

    aliases = json.load(open(a.aliases))
    URL_PREFIX.update(aliases.get("url_prefix", {}))
    ents = load_entities(a.site, aliases)
    if a.target:
        ents = [e for e in ents if e["path"] == a.target]
        if not ents:
            sys.exit(f"target {a.target} not found (posts need an entry in {a.aliases})")
    kinds = set(a.kinds.split(","))

    files = a.files or [os.path.join(a.site, "content", d, f)
                        for d, _ in DIRS
                        if os.path.isdir(os.path.join(a.site, "content", d))
                        for f in sorted(os.listdir(os.path.join(a.site, "content", d)))
                        if f.endswith(".mdx") and not f.startswith("_")]
    titles = {e["path"]: e["title"] for e in load_entities(a.site, aliases)
              if e["kind"] in FM_FIELD}
    report, total, applied, fm_added = {}, 0, 0, {}
    for fp in files:
        kind = dict(DIRS)[os.path.basename(os.path.dirname(fp))]
        fm, new_body, items = plan_file(fp, kind, ents, a.max_links, kinds, a.approve_review)
        if a.apply and kind == "post":
            nfm, added = sync_fm(fm, new_body, titles)
            if added and not any(x["apply"] for x in items):
                open(fp, "w").write(f"---\n{nfm}\n---\n" + new_body)
            if added:
                fm_added[os.path.relpath(fp, a.site)] = added
        items = [x for x in items if x["kind"] in kinds or x["review"]]
        if not items:
            continue
        rel = os.path.relpath(fp, a.site)
        report[rel] = items
        total += sum(1 for x in items if x["apply"])
        if a.apply and any(x["apply"] for x in items):
            n, _ = apply(fp, kind, fm, new_body, items, titles)
            applied += n

    if a.json:
        print(json.dumps(report, indent=1, ensure_ascii=False))
        return
    by_kind = {}
    for rel, items in report.items():
        print(f"\n{rel}")
        for x in items:
            tag = "REVIEW" if x["review"] else ("CAPPED" if x["capped"] else x["kind"])
            by_kind[tag] = by_kind.get(tag, 0) + 1
            print(f"  [{tag}] {x['text']!r} -> {x['target']}  ...{x['ctx']}...")
    print(f"\n{len(report)} files, {total} linkable mentions; by kind: {by_kind}")
    if a.apply:
        print(f"applied {applied} links")
        for rel, added in fm_added.items():
            print(f"frontmatter {rel}: + {', '.join(added)}")


if __name__ == "__main__":
    main()
