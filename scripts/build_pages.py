from __future__ import annotations

import base64
import gzip
import hashlib
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
PARTS = [
    "app/chunk00.b64",
    "app/chunk01a.b64",
    "app/chunk01b.b64",
    "app/chunk02.b64",
    "app/chunk03.b64",
    "app/chunk04.b64",
    "app/chunk05.b64",
    "app/chunk06.b64",
    "app/chunk07.b64",
]
EXPECTED_HTML_SHA256 = "6df9ea3f4e9bd5cfe290cae1c8b11169a55cf1fe079c7780ee899a778db5a7c2"

encoded = "".join("".join((ROOT / part).read_text(encoding="utf-8").split()) for part in PARTS)
compressed = base64.b64decode(encoded, validate=True)
html = gzip.decompress(compressed)
actual_sha256 = hashlib.sha256(html).hexdigest()
if actual_sha256 != EXPECTED_HTML_SHA256:
    raise SystemExit(
        f"Shieldfall payload checksum mismatch: {actual_sha256} != {EXPECTED_HTML_SHA256}"
    )

if SITE.exists():
    shutil.rmtree(SITE)
SITE.mkdir(parents=True)
(SITE / "index.html").write_bytes(html)

for name in ["manifest.webmanifest", "sw.js", "icon.svg", "icon-maskable.svg"]:
    shutil.copy2(ROOT / name, SITE / name)

(SITE / ".nojekyll").write_text("", encoding="utf-8")
print(f"Built Shieldfall Pages site: {len(html):,} bytes, sha256={actual_sha256}")
