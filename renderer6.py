import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1920
HEIGHT = 1080

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
        HEIGHT / image.height
    )

    new_width = int(image.width * scale)
    new_height = int(image.height * scale)

    image = image.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS
    )

    left = (new_width - WIDTH) // 2
    top = (new_height - HEIGHT) // 2

    return image.crop(
        (left, top, left + WIDTH, top + HEIGHT)
    )


def draw_text_box(
    draw,
    text,
    box,
    font,
    fill,
    align="left",
    vertical="center"
):
    x = box["x"]
    y = box["y"]
    width = box["width"]
    height = box["height"]

    bbox = draw.textbbox(
        (0, 0),
        text,
        font=font
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    if align == "center":
        text_x = x + (width - text_width) / 2

    elif align == "right":
        text_x = x + width - text_width

    else:
        text_x = x

    if vertical == "top":
        text_y = y - bbox[1]

    else:
        text_y = (
            y
            + (height - text_height) / 2
            - bbox[1]
        )

    draw.text(
        (text_x, text_y),
        text,
        font=font,
        fill=fill
    )


def main():

    if len(sys.argv) != 2:
        print("Usage: python renderer6.py input.json")
        sys.exit(1)

    input_file = Path(sys.argv[1])

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as f:
        data = json.load(f)

    work_dir = Path("work")
    work_dir.mkdir(exist_ok=True)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    background_path = work_dir / "background"
    logo_path = work_dir / "logo"

    # Background
    download_image(
        data["background"],
        background_path
    )

    background = Image.open(background_path)

    canvas = fit_background(background)

    # Logo
    download_image(
        data["logo"],
        logo_path
    )

    logo = Image.open(logo_path).convert("RGBA")

    logo = logo.resize(
        (150, 150),
        Image.Resampling.LANCZOS
    )

    canvas = canvas.convert("RGBA")

    canvas.alpha_composite(
        logo,
        (19, 19)
    )

    draw = ImageDraw.Draw(canvas)

    # -------------------------------------------------
    # Telegram :
    # -------------------------------------------------

    font = load_font(
        50,
        bold=True
    )

    draw_text_box(
        draw,
        "Telegram :",
        {
            "x": 52,
            "y": 962,
            "width": 211,
            "height": 77
        },
        font,
        "#000000",
        "left",
        "center"
    )

    # -------------------------------------------------
    # Channel
    # -------------------------------------------------

    channel = str(
        data.get(
            "channel",
            "https://t.me/qatufwdurar"
        )
    )

    font = load_font(
        40,
        bold=True
    )

    draw_text_box(
        draw,
        channel,
        {
            "x": 263,
            "y": 978,
            "width": 516,
            "height": 45
        },
        font,
        "#000000",
        "left",
        "top"
    )

    # -------------------------------------------------
    # المجلس
    # -------------------------------------------------

    font = load_font(
        50,
        bold=True
    )

    draw_text_box(
        draw,
        "المجلس",
        {
            "x": 1658,
            "y": 975,
            "width": 170,
            "height": 50
        },
        font,
        "#303030",
        "right",
        "top"
    )

    # -------------------------------------------------
    # Episode
    # -------------------------------------------------

    episode = str(
        data.get(
            "episode",
            "93"
        )
    )

    font = load_font(
        50,
        bold=True
    )

    draw_text_box(
        draw,
        episode,
        {
            "x": 1544,
            "y": 970,
            "width": 114,
            "height": 61
        },
        font,
        "#262626",
        "right",
        "center"
    )

    # -------------------------------------------------
    # Title
    # -------------------------------------------------

    title = str(
        data.get(
            "title",
            "التِّبيان لجَرْدِ الكُتبِ والمُطوَّلَات"
        )
    )

    font = load_font(
        60,
        bold=True
    )

    draw_text_box(
        draw,
        title,
        {
            "x": 779,
            "y": 58,
            "width": 1073,
            "height": 503
        },
        font,
        "#282828",
        "center",
        "center"
    )

    # -------------------------------------------------
    # الشيخ عبد الكريم الكثيري حفظه الله
    # -------------------------------------------------

    font = load_font(
        50,
        bold=True
    )

    draw_text_box(
        draw,
        "الشيخ عبد الكريم الكثيري حفظه الله",
        {
            "x": 779,
            "y": 965,
            "width": 776,
            "height": 71
        },
        font,
        "#000000",
        "center",
        "top"
    )

    # -------------------------------------------------
    # Save
    # -------------------------------------------------

    output_file = output_dir / "output.png"

    canvas.convert("RGB").save(
        output_file,
        "PNG"
    )

    print(
        f"Image created: {output_file}"
    )


if __name__ == "__main__":
    main()
