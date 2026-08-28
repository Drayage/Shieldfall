from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CARDS_DIR = ROOT / "assets" / "cards"
CARD_SIZE = (640, 960)


def prepare_cards(cards_dir: Path) -> list[Path]:
    outputs: list[Path] = []
    for source in sorted(cards_dir.glob("*.png")):
        target = source.with_suffix(".webp")
        with Image.open(source) as image:
            normalized = ImageOps.fit(
                image.convert("RGB"),
                CARD_SIZE,
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5),
            )
            normalized.save(target, "WEBP", quality=84, method=6)
        outputs.append(target)
    return outputs


def make_contact_sheet(images: list[Path], target: Path) -> None:
    columns = 7
    thumb_size = (160, 240)
    label_height = 24
    rows = (len(images) + columns - 1) // columns
    sheet = Image.new(
        "RGB",
        (columns * thumb_size[0], rows * (thumb_size[1] + label_height)),
        "#0d1117",
    )
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=13)

    for index, image_path in enumerate(images):
        column = index % columns
        row = index // columns
        x = column * thumb_size[0]
        y = row * (thumb_size[1] + label_height)
        with Image.open(image_path) as image:
            thumb = ImageOps.fit(
                image.convert("RGB"),
                thumb_size,
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5),
            )
            sheet.paste(thumb, (x, y))
        draw.text((x + 6, y + thumb_size[1] + 5), image_path.stem, font=font, fill="#f0f6fc")

    target.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(target, "JPEG", quality=88, optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize Shieldfall card art for mobile delivery.")
    parser.add_argument("--cards-dir", type=Path, default=DEFAULT_CARDS_DIR)
    parser.add_argument("--contact-sheet", type=Path)
    args = parser.parse_args()

    outputs = prepare_cards(args.cards_dir)
    if not outputs:
        raise SystemExit(f"No PNG card art found in {args.cards_dir}")
    if args.contact_sheet:
        make_contact_sheet(outputs, args.contact_sheet)

    total_bytes = sum(path.stat().st_size for path in outputs)
    print(f"Prepared {len(outputs)} cards at {CARD_SIZE[0]}x{CARD_SIZE[1]} ({total_bytes:,} bytes)")


if __name__ == "__main__":
    main()
