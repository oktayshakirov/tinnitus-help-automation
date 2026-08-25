#!/usr/bin/env python3
"""Deterministic quality gate for a tinnitushelp.me post MDX (skill Step 3).

Usage:
  python3 quality_gate.py <post.mdx> [--db <content-database.json>]
      [--archive <image dir>]

Runs every Step-3 check and prints one line per check (PASS / WARN / FAIL).
Exits non-zero if any hard FAIL is found (WARN does not fail the gate).

Tinnitus Help only. For thecrypto.wiki use publish-content-crypto's own copy
of this script in crypto-wiki-automation - the two sites differ in almost
every surface detail (link prefixes, image syntax, ad component, frontmatter
quoting, whether an author field exists), which is why this is a separate
script rather than one shared script branching on site.
"""
import argparse, json, os, re, sys
from datetime import datetime

DB = "/Users/oktayshakirov/Coding/tinnitus-help-automation/content-database.json"
ARCHIVE = "/Users/oktayshakirov/Coding/tinnitus-blog/public/images"
DOMAIN = "https://www.tinnitushelp.me"
STATIC = {"/app", "/about", "/contact", "/faq", "/privacy", "/terms",
          "/disclaimer", "/blog", "/zen"}

# Domains already established across the archive as citable primary sources.
# Anything outside this set WARNs rather than FAILs - widen it deliberately.
SOURCE_DOMAINS = {
    "nidcd.nih.gov",          # National Institute on Deafness (NIH)
    "entnet.org",             # AAO-HNS clinical practice guidelines
    "ata.org",                # American Tinnitus Association
    "nhs.uk",
    "who.int",
    "mayoclinic.org",
    "cochrane.org",
    "ncbi.nlm.nih.gov",
    "pubmed.ncbi.nlm.nih.gov",
    "pmc.ncbi.nlm.nih.gov",
    "ods.od.nih.gov",
    "nih.gov",
    "cdc.gov",
}

# curl notes for verifying these: pubmed returns 203, not 200 (bot mitigation
# on a live page) and ods.od.nih.gov returns 403 to curl entirely. Treat any
# 2xx as live, and check an ods link in a browser rather than assuming it 404s.

# Tags that mark a culture/history post rather than a health one. Those set
# medical: false, which drops the MedicalWebPage typing and the clinical
# disclaimer - a disclaimer on an art-history piece is just noise.
CULTURE_TAGS = {"history", "society"}

# post_guidelines.md fixes this list; the Build node should emit only these.
TAGS = {"basics", "management", "research", "psychology",
        "nutrition", "meditation", "sounds"}
# Tags that predate that list but are live on the site with real tag pages
# (lifestyle x15, society x13, technology x7, neuroscience x6, history x3), and
# that the workflow still emits. Accepted with a WARN so a genuinely invented
# tag still FAILs; widen TAGS if the guidelines adopt them.
TAGS_LEGACY = {"lifestyle", "society", "technology", "neuroscience", "history"}

FAIL, WARN, PASS = "FAIL", "WARN", "PASS"
results = []  # (level, check, detail)


def record(level, check, detail=""):
    results.append((level, check, detail))


def check(cond, name, ok_detail="ok", bad_detail="", level=FAIL):
    record(PASS if cond else level, name, ok_detail if cond else bad_detail)


# Content directory -> URL prefix. Note posts serve at /blog/, not /posts/.
CONTENT_DIRS = {"posts": "/blog/", "zen": "/zen/"}


def valid_slugs(db, mdx_path):
    """Set of valid internal link targets.

    Union of the content DB and the MDX actually on disk. The DB drifts (two
    live posts are missing from it), and a link to a page that really exists
    must not fail the gate.
    """
    out = set(STATIC)

    for key, pref in (("blog", "/blog/"), ("zen", "/zen/")):
        for v in db.get(key, {}).values():
            s = (v.get("slug") or "").lstrip("/")
            if s.startswith(("posts/", "exchanges/", "crypto-ogs/", "tools/")):
                out.add("/" + s)
            else:
                out.add(pref + s)

    # ...plus whatever is actually published in the site repo's content tree.
    content_root = os.path.dirname(os.path.dirname(os.path.abspath(mdx_path)))
    for sub, pref in CONTENT_DIRS.items():
        d = os.path.join(content_root, sub)
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if fn.endswith(".mdx") and not fn.startswith("_"):
                out.add(pref + fn[:-4])
    return out


def imgs_in(txt):
    return re.findall(r'<Image\s[^>]*src="(/images/[^"]+)"', txt)


def strip_tables(txt):
    """Drop markdown table separator rows (| --- | --- |).

    Legitimate table syntax (12 posts use tables), but looks like a banned
    `--` to the dash check.
    """
    return "\n".join(ln for ln in txt.split("\n")
                     if not re.match(r"^\s*\|[\s:|-]+\|\s*$", ln))


def fm_block(fm, key):
    """Lines belonging to a top-level frontmatter list, e.g. `sources:`.

    No YAML parser here (none is guaranteed on this machine and the rest of
    this script is regex anyway): take the lines after `key:` that are indented
    or start a list item, stop at the next top-level key.
    """
    m = re.search(rf"^{key}:[ \t]*$", fm, re.M)
    if not m:
        return None
    out = []
    for ln in fm[m.end():].split("\n")[1:]:
        if ln.strip() and not ln[:1].isspace():
            break
        out.append(ln)
    return "\n".join(out)


def domain_of(url):
    m = re.match(r"https?://([^/]+)", url.strip())
    if not m:
        return ""
    host = m.group(1).lower()
    # Prefix removal, not lstrip() - lstrip takes a character set and would
    # turn "who.int" into "ho.int".
    return host[4:] if host.startswith("www.") else host


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mdx")
    ap.add_argument("--db", default=DB)
    ap.add_argument("--archive", default=ARCHIVE)
    ap.add_argument("--recent-window", type=int, default=5,
                    help="how many of the most recent other posts to check for "
                         "repeated body images (reuse is fine, just not back to back)")
    a = ap.parse_args()

    record(PASS, "type", "tinnitus-post")

    text = open(a.mdx, encoding="utf-8").read()
    parts = text.split("---", 2)
    if len(parts) < 3:
        record(FAIL, "frontmatter", "no --- frontmatter block")
        emit_and_exit()
    fm, body = parts[1], parts[2]
    db = json.load(open(a.db))

    # --- word count ---
    words = len(re.findall(r"\b[\w'-]+\b",
                           re.sub(r"<[^>]+>|!\[.*?\]\(.*?\)", "", body)))
    record(PASS if 1200 <= words <= 2500 else WARN, "word count",
           f"{words} (target 1,200-2,500)")

    # --- description length: target 120-135, HARD max 140 (site truncates) ---
    m = re.search(r"""description:\s*(['"])(.*)\1""", fm)
    if m:
        desc = m.group(2)
        dl = len(desc)
        if dl > 140:
            record(FAIL, "description length",
                   f"{dl} chars (HARD max 140, target 120-135)")
        else:
            record(PASS if 120 <= dl <= 135 else WARN, "description length",
                   f"{dl} chars (target 120-135)")
    else:
        desc = ""
        record(FAIL, "description", "missing description in frontmatter")

    # --- tags: exactly 2-3, lowercase, from the fixed vocab ---
    mt = re.search(r"^tags:\s*\[(.*?)\]", fm, re.M)
    tags = [x.strip().strip("\"'") for x in mt.group(1).split(",")
            if x.strip()] if mt else []
    bad = [t for t in tags if t not in TAGS and t not in TAGS_LEGACY]
    legacy = [t for t in tags if t in TAGS_LEGACY]
    if bad or not 2 <= len(tags) <= 3:
        record(FAIL, "tags", f"{len(tags)} tags" +
               ("; not in vocab: " + ", ".join(bad) if bad else ""))
    else:
        record(WARN if legacy else PASS, "tags", ", ".join(tags) +
               ("  (legacy, outside guidelines vocab: "
                + ", ".join(legacy) + ")" if legacy else ""))

    # --- medical typing (culture/history posts opt out) ---
    # Defaults to true, which types the page MedicalWebPage and renders the
    # clinical disclaimer. Right for health posts, wrong on an art-history one.
    is_medical = not re.search(r"^medical:\s*false\b", fm, re.M)
    if is_medical and (set(tags) & CULTURE_TAGS):
        record(WARN, "medical typing",
               f"tags {sorted(set(tags) & CULTURE_TAGS)} look like a culture/history "
               "post - set `medical: false` unless it really makes health claims")
    else:
        record(PASS, "medical typing",
               "medical (default)" if is_medical else "medical: false (culture/history)")

    # --- sources: REQUIRED on health posts (YMYL / E-E-A-T) ---
    # Renders the References list. Every post generated in 2026 shipped without
    # one, including serotonin-and-tinnitus, which discussed SSRI tapering and
    # cited nothing. Optional on culture/history posts.
    src_block = fm_block(fm, "sources")
    urls = re.findall(r"^\s*url:\s*['\"]?([^'\"\n]+)", src_block or "", re.M)
    titles = re.findall(r"^\s*-\s*title:", src_block or "", re.M)
    if not is_medical:
        record(PASS, "sources", f"{len(urls)} (optional on culture/history posts)")
    elif not urls:
        record(FAIL, "sources",
               "none - a health post needs 3-5 authoritative sources "
               "(see Step 3b in the skill)")
    else:
        record(PASS if 3 <= len(urls) <= 5 else WARN, "sources count",
               f"{len(urls)} (target 3-5)")
        if len(titles) != len(urls):
            record(FAIL, "sources shape",
                   f"{len(titles)} title: vs {len(urls)} url: - every entry needs both")
        off = sorted({d for d in (domain_of(u) for u in urls)
                      if d and d not in SOURCE_DOMAINS})
        record(PASS if not off else WARN, "source domains",
               "all authoritative" if not off
               else "outside the known-authoritative set: " + ", ".join(off))
        nohttps = [u for u in urls if not u.strip().startswith("https://")]
        check(not nohttps, "sources are https",
              bad_detail="not https: " + ", ".join(nohttps))

    # --- faq: REQUIRED, feeds FaqSection + FAQPage JSON-LD ---
    faq_block = fm_block(fm, "faq")
    questions = re.findall(r"^\s*-\s*question:", faq_block or "", re.M)
    answers = re.findall(r"^\s*answer:", faq_block or "", re.M)
    if not questions:
        record(FAIL, "faq",
               "none - 4-5 entries required (renders FaqSection + FAQPage JSON-LD)")
    else:
        record(PASS if 4 <= len(questions) <= 5 else WARN, "faq count",
               f"{len(questions)} (target 4-5)")
        check(len(answers) == len(questions), "faq shape",
              f"{len(questions)} Q/A pairs",
              f"{len(questions)} question: vs {len(answers)} answer:")
        # The JSON-LD takes the plain answer string, so markdown links in an
        # answer ship as literal brackets into the structured data.
        md = [q for q in re.findall(r"^\s*answer:\s*(.*)$", faq_block or "", re.M)
              if re.search(r"\[[^\]]+\]\(", q)]
        record(PASS if not md else WARN, "faq answers are plain text",
               "ok" if not md else f"{len(md)} answer(s) contain markdown links")

    # --- links: count, dedupe, bold, slug validity ---
    links = re.findall(r"\[([^\]]+)\]\((/[^)]+)\)", body)
    internal = [(t, u) for t, u in links if not u.startswith("/images/")]
    record(PASS if 8 <= len(internal) <= 15 else WARN, "internal link count",
           f"{len(internal)} (target 8-15)")

    seen, dups = set(), set()
    for _, u in internal:
        (dups if u in seen else seen).add(u)
    check(not dups, "no duplicate links",
          bad_detail="dupes: " + ", ".join(sorted(dups)))

    bold = set(re.findall(r"\*\*\[[^\]]+\]\((/[^)]+)\)\*\*", body))
    notbold = [u for _, u in internal if u not in bold]
    check(not notbold, "links bolded",
          bad_detail="not bold: " + ", ".join(notbold))

    valid = valid_slugs(db, a.mdx)
    # Strip #anchors and ?query - a deep link into a real page is still valid.
    invalid = [u for _, u in internal
               if u.split("#")[0].split("?")[0].rstrip("/") not in valid]
    check(not invalid, "slugs valid vs DB",
          bad_detail="invalid: " + ", ".join(invalid))

    # --- images: exactly 2 <Image />, and the FIRST one is the main image ---
    mi = re.search(r"""image:\s*(['"])([^'"]+)\1""", fm)
    main_img = mi.group(2) if mi else ""
    body_imgs = imgs_in(body)

    check(len(body_imgs) == 2, "exactly 2 images",
          f"{len(body_imgs)} found", f"{len(body_imgs)} found")
    check(bool(main_img) and bool(body_imgs) and body_imgs[0] == main_img,
          "first image is the main image", main_img,
          f"main={main_img or 'none'}, "
          f"first={body_imgs[0] if body_imgs else 'none'}")
    extra = body_imgs[1:]

    missing = [q for q in body_imgs
               if not os.path.exists(os.path.join(a.archive, os.path.basename(q)))]
    check(not missing, "images exist in archive",
          bad_detail=f"missing from {a.archive}: " + ", ".join(missing))

    # --- shared images not repeated in nearby posts ---
    # Reusing an archive image is fine and expected. What is not fine is reusing
    # it in posts published close together, because someone reading a few in a
    # row sees the same picture twice (audiologist.jpg was the body image on
    # three consecutive posts). So compare only against the N most recent OTHER
    # posts, by frontmatter date, not the archive as a whole. The main image is
    # slug-specific and never shared, so it is excluded.
    def post_date(txt):
        d = re.search(r"^date:\s*['\"]?([^'\"\n]+)['\"]?\s*$", txt, re.M)
        if not d:
            return None
        raw = d.group(1).strip()
        for fmt in ("%Y-%m-%d", "%B %d, %Y", "%b %d, %Y"):
            try:
                return datetime.strptime(raw, fmt)
            except ValueError:
                continue
        return None

    mine = set(extra) - {main_img}
    content_dir = os.path.dirname(os.path.abspath(a.mdx))
    others = []
    for fn in os.listdir(content_dir):
        if not fn.endswith(".mdx") or fn == os.path.basename(a.mdx) or fn.startswith("_"):
            continue
        txt = open(os.path.join(content_dir, fn), encoding="utf-8", errors="ignore").read()
        dt = post_date(txt)
        if dt:
            others.append((dt, fn, txt))
    others.sort(reverse=True)

    clashes = []
    for dt, fn, txt in others[:a.recent_window]:
        used = set(imgs_in(txt))
        for q in sorted(mine & used):
            clashes.append(f"{os.path.basename(q)} also in {fn[:-4]} ({dt:%Y-%m-%d})")
    record(PASS if not clashes else WARN,
           f"images not reused in last {a.recent_window} posts",
           "ok" if not clashes else "; ".join(clashes))

    # --- dashes / curly quotes (body + user-facing description) ---
    hygiene = strip_tables(body) + "\n" + desc
    bad_dash = [c for c in ("—", "–") if c in hygiene] + (["--"] if "--" in hygiene else [])
    check(not bad_dash, "no em/en/-- dashes",
          bad_detail="found: " + " ".join(bad_dash))

    curly = {c: hygiene.count(c) for c in "‘’“”" if hygiene.count(c)}
    check(not curly, "no curly quotes",
          bad_detail=", ".join(f"{k}x{v}" for k, v in curly.items()))

    # --- metadata / references ---
    record(PASS if not re.search(r"```[\s\S]*\{[\s\S]*\}[\s\S]*```\s*$", body)
           and not re.search(r"^\s*\{[\s\S]*\}\s*$", body.strip()[-400:] or "x")
           else WARN, "no trailing metadata JSON", "ok")

    check(not re.search(r"^#+\s*References\b", body, re.M), "no References section")

    # --- structure: <Blockquote> -> main <Image> -> ## <Highlighter> ---
    check(body.lstrip().startswith("<Blockquote>"), "opens with <Blockquote>",
          bad_detail="body does not start with <Blockquote>")
    heads = re.findall(r"^##\s+(.*)$", body, re.M)
    check(bool(heads) and heads[0].startswith("<Highlighter>"),
          "first ## uses <Highlighter>",
          bad_detail=f"first ## is: {heads[0][:60] if heads else 'none'}")
    plain = [h for h in heads if not h.startswith("<Highlighter>")]
    record(PASS if not plain else WARN, "all ## use <Highlighter>",
           "ok" if not plain
           else f"{len(plain)} plain: " + "; ".join(h[:40] for h in plain))
    # Headless intro: prose between the main <Image> and the first heading.
    mimg = re.search(r"<Image\s[^>]*>", body)
    mhead = re.search(r"^##\s", body, re.M)
    if mimg and mhead and mhead.start() > mimg.end():
        between = body[mimg.end():mhead.start()].strip()
        check(not between, "no headless intro before first heading",
              bad_detail="prose sits between the main image and the first "
                         f"heading: {between[:70]}...")

    # --- ads present + not adjacent to images ---
    check("AdComponent" in body, "<AdComponent /> present",
          bad_detail="no AdComponent in body")

    sig = [(i, ln) for i, ln in enumerate(body.split("\n"))
           if "AdComponent" in ln or "<Image" in ln]
    adj = []
    for (i1, l1), (i2, l2) in zip(sig, sig[1:]):
        k1 = "AD" if "AdComponent" in l1 else "IMG"
        k2 = "AD" if "AdComponent" in l2 else "IMG"
        if k1 != k2 and i2 - i1 <= 2:
            adj.append(f"lines {i1+1}->{i2+1}")
    check(not adj, "ads not adjacent to images", bad_detail="; ".join(adj))

    emit_and_exit()


def emit_and_exit():
    icon = {PASS: "✓", WARN: "⚠", FAIL: "✗"}
    for level, chk, detail in results:
        print(f"  {icon[level]} {level:4} {chk}" + (f" - {detail}" if detail else ""))
    fails = sum(1 for l, _, _ in results if l == FAIL)
    warns = sum(1 for l, _, _ in results if l == WARN)
    print(f"\n{'FAILED' if fails else 'PASSED'}: {fails} fail, {warns} warn, "
          f"{len(results)} checks")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
