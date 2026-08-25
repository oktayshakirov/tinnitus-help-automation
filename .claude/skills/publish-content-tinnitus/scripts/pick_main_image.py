#!/usr/bin/env python3
"""Fetch main-image candidates from Pexels, resize to the site standard, and
stage them for the user to pick one.

Usage:
  python3 pick_main_image.py --query "dramatic low key portrait side profile" \
      --slug how-tinnitus-affects-sleep --out <preview_dir> \
      [--width 800] [--count 3] [--page 1] [--orientation landscape]

Writes <out>/candidate_1.jpg .. candidate_N.jpg (resized JPEGs, each < 200 KB)
and prints a JSON manifest to stdout: [{n, file, kb, photographer, source_url}].
Re-roll with a higher --page to get different results for the same query.

Key: reads the Pexels API key from crypto-wiki-automation/.pexels-api-key
(gitignored - shared across both sites, lives in the crypto repo, not this
one). Get a free key at https://www.pexels.com/api/.
"""
import argparse, json, os, subprocess, sys, urllib.request, urllib.parse

KEY_PATH = "/Users/oktayshakirov/Coding/crypto-wiki-automation/.pexels-api-key"


def load_key():
    if not os.path.exists(KEY_PATH):
        sys.exit(f"ERROR: no Pexels key at {KEY_PATH}. Create it (gitignored) with a "
                 "free key from https://www.pexels.com/api/.")
    k = open(KEY_PATH).read().strip()
    if not k:
        sys.exit(f"ERROR: {KEY_PATH} is empty.")
    return k


def search(key, query, per_page, page, orientation):
    qs = urllib.parse.urlencode({
        "query": query, "per_page": per_page, "page": page,
        "orientation": orientation,
    })
    req = urllib.request.Request(
        "https://api.pexels.com/v1/search?" + qs,
        headers={"Authorization": key, "User-Agent": "publish-content/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "publish-content/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        f.write(r.read())


def resize_jpeg(src, dst, width):
    """Downscale to `width` (px) preserving aspect, re-encode JPEG, keep < 200 KB."""
    for quality in (80, 70, 60, 50, 40):
        subprocess.run(["sips", "--resampleWidth", str(width),
                        "-s", "format", "jpeg", "-s", "formatOptions", str(quality),
                        src, "--out", dst],
                       check=True, capture_output=True)
        if os.path.getsize(dst) <= 200 * 1024:
            return quality
    return quality  # smallest we tried; still emit it


def ahash(path):
    """64-bit average hash via `sips` (no PIL on this machine).

    Pexels re-serves its popular stock repeatedly, so a candidate is often a
    photo already sitting in the site archive under another slug. Downsample
    to an 8x8 BMP, parse the pixel array, threshold against the mean.
    """
    import struct, tempfile
    with tempfile.TemporaryDirectory() as td:
        bmp = os.path.join(td, "t.bmp")
        r = subprocess.run(
            ["sips", "-s", "format", "bmp", "-z", "8", "8", path, "--out", bmp],
            capture_output=True,
        )
        if r.returncode != 0 or not os.path.exists(bmp):
            return None
        d = open(bmp, "rb").read()
    off = struct.unpack_from("<I", d, 10)[0]
    npx = struct.unpack_from("<H", d, 28)[0] // 8
    row = ((npx * 8 * 8 + 31) // 32) * 4
    px = []
    for y in range(8):
        base = off + y * row
        for x in range(8):
            b, g, r_ = d[base + x * npx], d[base + x * npx + 1], d[base + x * npx + 2]
            px.append(0.299 * r_ + 0.587 * g + 0.114 * b)
    avg = sum(px) / 64
    bits = 0
    for i, v in enumerate(px):
        if v >= avg:
            bits |= 1 << i
    return bits


def archive_hashes(archive_dir):
    out = {}
    if not archive_dir or not os.path.isdir(archive_dir):
        return out
    for f in sorted(os.listdir(archive_dir)):
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            h = ahash(os.path.join(archive_dir, f))
            if h is not None:
                out[f] = h
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--out", required=True, help="preview dir for candidates")
    ap.add_argument("--width", type=int, default=800)
    ap.add_argument("--count", type=int, default=3)
    ap.add_argument("--page", type=int, default=1)
    ap.add_argument("--orientation", default="landscape")
    ap.add_argument("--archive", default=None,
                    help="site image dir to reject already-used photos against "
                         "(tinnitus-blog/public/images)")
    ap.add_argument("--dup-threshold", type=int, default=6,
                    help="max aHash Hamming distance treated as the same photo")
    a = ap.parse_args()

    key = load_key()
    os.makedirs(a.out, exist_ok=True)
    raw = os.path.join(a.out, "_raw")
    os.makedirs(raw, exist_ok=True)

    data = search(key, a.query, max(a.count * 3, 9), a.page, a.orientation)
    photos = data.get("photos", [])
    if not photos:
        sys.exit(f"No Pexels results for {a.query!r} (page {a.page}). Try another query.")

    arch = archive_hashes(a.archive)
    manifest, skipped, i = [], [], 0
    for p in photos:
        if len(manifest) >= a.count:
            break
        i += 1
        src_url = p["src"].get("large2x") or p["src"].get("large") or p["src"]["original"]
        tmp = os.path.join(raw, f"src_{i}.jpg")
        n = len(manifest) + 1
        out = os.path.join(a.out, f"candidate_{n}.jpg")
        download(src_url, tmp)
        resize_jpeg(tmp, out, a.width)

        if arch:
            h = ahash(out)
            if h is not None:
                near = min(((bin(h ^ v).count("1"), k) for k, v in arch.items()),
                           default=(99, ""))
                if near[0] <= a.dup_threshold:
                    skipped.append({"already_in_archive_as": near[1],
                                    "distance": near[0],
                                    "source_url": p.get("url", "")})
                    os.remove(out)
                    continue

        manifest.append({
            "n": n,
            "file": out,
            "kb": round(os.path.getsize(out) / 1024, 1),
            "photographer": p.get("photographer", ""),
            "source_url": p.get("url", ""),
            "alt": p.get("alt", ""),
        })

    if skipped:
        print(json.dumps({"skipped_duplicates": skipped}, indent=1), file=sys.stderr)
    print(json.dumps(manifest, indent=1))


if __name__ == "__main__":
    main()
