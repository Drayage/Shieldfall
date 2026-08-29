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
EXPECTED_HTML_SHA256 = "8525dd4390c383da586b4b7116a27fc11765ddf6de3a3c963d8d9e797f9ecddf"

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

shutil.copytree(ROOT / "assets", SITE / "assets")

(SITE / ".nojekyll").write_text("", encoding="utf-8")
print(f"Built Shieldfall Pages site: {len(html):,} bytes, sha256={actual_sha256}")
