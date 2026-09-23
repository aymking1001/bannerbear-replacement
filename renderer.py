import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1920
HEIGHT = 1080


# Temporary fonts.
# We will replace these later with the exact fonts.
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load_font(size, bold=False):
    font_path = FONT_BOLD if bold else FONT_REGULAR
    return ImageFont.truetype(font_path, size)


def download_image(url, path):
    import urllib.request

    urllib.request.urlretrieve(url, path)


def fit_background(image):
    image = image.convert("RGB")

    scale = max(
        WIDTH / image.width,
        HEIGHT / image.height,
    )

    new_width = int(image.width * scale)
    new_height = int(image.height * scale)

    image = image.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS,
    )

    left = (new_width - WIDTH) // 2
    top = (new_height - HEIGHT) // 2

    return image.crop(
        (
            left,
            top,
            left + WIDTH,
            top + HEIGHT,
        )
    )


def draw_text_box(
    draw,
    text,
    box,
    font,
    fill,
    align="left",
):
    x = box["x"]
    y = box["y"]
    width = box["width"]
    height = box["height"]

    bbox = draw.textbbox(
        (0, 0),
        text,
        font=font,
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    if align == "center":
        text_x = x + (width - text_width) / 2
    else:
        text_x = x

    text_y = y + (height - text_height) / 2 - bbox[1]

    draw.text(
        (text_x, text_y),
        text,
        font=font,
        fill=fill,
    )


def main():
    if len(sys.argv) != 2:
        print("Usage: python renderer.py input.json")
        sys.exit(1)

    input_file = Path(sys.argv[1])

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    work_dir = Path("work")
    work_dir.mkdir(exist_ok=True)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    background_path = work_dir / "background"
    logo_path = work_dir / "logo"

    # ---------------------------------------------------------
    # 1. Background
    # ---------------------------------------------------------

    download_image(
        data["background"],
        background_path,
    )

    background = Image.open(background_path)
    canvas = fit_background(background)

    # ---------------------------------------------------------
    # 2. Logo
    # ---------------------------------------------------------

    download_image(
        data["logo"],
        logo_path,
    )

    logo = Image.open(logo_path).convert("RGBA")

    logo = logo.resize(
        (150, 150),
        Image.Resampling.LANCZOS,
    )

    canvas = canvas.convert("RGBA")

    canvas.alpha_composite(
        logo,
        (19, 19),
    )

    draw = ImageDraw.Draw(canvas)

    # ---------------------------------------------------------
    # 3. Fixed text: text_container_9
    # ---------------------------------------------------------

    font = load_font(
        149,
        bold=True,
    )

    draw_text_box(
        draw,
        ": المجلس",
        {
            "x": 997,
            "y": 454,
            "width": 480,
            "height": 308,
        },
        font,
        "#000000",
        "center",
    )

    # ---------------------------------------------------------
    # 4. Fixed text: text_container_6
    # ---------------------------------------------------------

    font = load_font(
        88,
        bold=True,
    )

    draw_text_box(
        draw,
        "Telegram :",
        {
            "x": 539,
            "y": 711,
            "width": 331,
            "height": 159,
        },
        font,
        "#000000",
        "left",
    )

    # ---------------------------------------------------------
    # 5. Episode
    # ---------------------------------------------------------

    episode = str(data.get("episode", "20"))

    font = load_font(
        50,
        bold=True,
    )

    draw_text_box(
        draw,
        episode,
        {
            "x": 585,
            "y": 568,
            "width": 238,
            "height": 81,
        },
        font,
        "#000000",
        "center",
    )

    # ---------------------------------------------------------
    # 6. Title
    # ---------------------------------------------------------

    title = str(
        data.get(
            "title",
            "التِّبيان لجَرْدِ الكُتبِ و المُطوَّلَات",
        )
    )

    font = load_font(
        99,
        bold=True,
    )

    draw_text_box(
        draw,
        title,
        {
            "x": 538,
            "y": 150,
            "width": 845,
            "height": 418,
        },
        font,
        "#000000",
        "center",
    )

    # ---------------------------------------------------------
    # 7. Channel
    # ---------------------------------------------------------

    channel = str(
        data.get(
            "channel",
            "https://t.me/qatufwdurar",
        )
    )

    font = load_font(
        45,
        bold=False,
    )

    draw_text_box(
        draw,
        channel,
        {
            "x": 1047,
            "y": 749,
            "width": 822,
            "height": 84,
        },
        font,
        "#000000",
        "left",
    )

    # ---------------------------------------------------------
    # 8. Save
    # ---------------------------------------------------------

    output_file = output_dir / "output.png"

    canvas.convert("RGB").save(
        output_file,
        "PNG",
    )

    print(f"Image created: {output_file}")


if __name__ == "__main__":
    main()
