from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import math
import re
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEGACY_CARD_ART_START = b"const CARD_ART_SPEC={"
CURRENT_CARD_ART_START = b"function cardArtPath(def)"
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


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1)
    if count != 1:
        raise SystemExit(f"Could not update {label}; expected exactly one match, found {count}")
    return updated


def main() -> None:
    parser = argparse.ArgumentParser(description="Pack a Shieldfall HTML source into deployable chunks.")
    parser.add_argument("source", type=Path, help="Path to the complete Shieldfall HTML file")
    args = parser.parse_args()

    html = args.source.read_bytes()
    legacy_start = html.find(LEGACY_CARD_ART_START)
    if legacy_start >= 0:
        current_start = html.find(CURRENT_CARD_ART_START, legacy_start)
        if current_start < 0:
            raise SystemExit("Found legacy SVG card art without the current bitmap renderer")
        html = html[:legacy_start] + html[current_start:]
    html_sha256 = hashlib.sha256(html).hexdigest()
    encoded = base64.b64encode(gzip.compress(html, compresslevel=9, mtime=0)).decode("ascii")
    part_size = math.ceil(len(encoded) / len(PARTS))

    for index, relative_path in enumerate(PARTS):
        part = encoded[index * part_size : (index + 1) * part_size]
        wrapped = "\n".join(textwrap.wrap(part, width=76)) + "\n"
        (ROOT / relative_path).write_text(wrapped, encoding="utf-8", newline="\n")

    build_script_path = ROOT / "scripts" / "build_pages.py"
    build_script = build_script_path.read_text(encoding="utf-8")
    build_script = replace_once(
        build_script,
        r'EXPECTED_HTML_SHA256 = "[0-9a-f]{64}"',
        f'EXPECTED_HTML_SHA256 = "{html_sha256}"',
        "build checksum",
    )
    build_script_path.write_text(build_script, encoding="utf-8", newline="\n")

    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    readme = replace_once(
        readme,
        r'(현재 검증 대상 HTML SHA-256:\s*`)[0-9a-f]{64}(`)',
        rf'\g<1>{html_sha256}\g<2>',
        "README checksum",
    )
    readme_path.write_text(readme, encoding="utf-8", newline="\n")

    print(
        f"Packed {len(html):,} HTML bytes into {len(PARTS)} chunks "
        f"({len(encoded):,} base64 characters), sha256={html_sha256}"
    )


if __name__ == "__main__":
    main()
