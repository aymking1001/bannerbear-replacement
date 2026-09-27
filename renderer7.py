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


def draw_auto_fit_text(
    draw,
    text,
    box,
    max_font_size,
    fill,
    bold=False,
    align="left",
    vertical="center",
    min_font_size=1
):
    x = box["x"]
    y = box["y"]
    width = box["width"]
    height = box["height"]

    text = str(text)

    font_size = max_font_size

    while font_size >= min_font_size:
        font = load_font(
            font_size,
            bold=bold
        )

        bbox = draw.multiline_textbbox(
            (0, 0),
            text,
            font=font,
            align=align,
            spacing=0
        )

        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        if (
            text_width <= width
            and text_height <= height
        ):
            break

        font_size -= 1

    font = load_font(
        max(font_size, min_font_size),
        bold=bold
    )

    bbox = draw.multiline_textbbox(
        (0, 0),
        text,
        font=font,
        align=align,
        spacing=0
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

    elif vertical == "bottom":
        text_y = y + height - text_height - bbox[1]

    else:
        text_y = (
            y
            + (height - text_height) / 2
            - bbox[1]
        )

    draw.multiline_text(
        (text_x, text_y),
        text,
        font=font,
        fill=fill,
        align=align,
        spacing=0
    )


def main():

    if len(sys.argv) != 2:
        print("Usage: python renderer7.py input.json")
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

    # -------------------------------------------------
    # Background
    # -------------------------------------------------

    download_image(
        data["background"],
        background_path
    )

    background = Image.open(background_path)

    canvas = fit_background(background)

    # -------------------------------------------------
    # Logo
    # -------------------------------------------------

    download_image(
        data["logo"],
        logo_path
    )

    logo = Image.open(logo_path).convert("RGBA")

    logo = logo.resize(
        (150, 138),
        Image.Resampling.LANCZOS
    )

    canvas = canvas.convert("RGBA")

    canvas.alpha_composite(
        logo,
        (19, 19)
    )

    draw = ImageDraw.Draw(canvas)

    TEXT_COLOR = "#270D30"

    # -------------------------------------------------
    # Title
    # -------------------------------------------------

    title = str(
        data.get(
            "title",
            "التِّبيان لجَرْدِ الكُتبِ والمُطوَّلَات"
        )
    )

    draw_auto_fit_text(
        draw,
        title,
        {
            "x": 592,
            "y": 419,
            "width": 736,
            "height": 418
        },
        50,
        TEXT_COLOR,
        bold=False,
        align="center",
        vertical="center"
    )

    # -------------------------------------------------
    # CTA
    # -------------------------------------------------

    cta_box = {
        "x": 698,
        "y": 911,
        "width": 525,
        "height": 64
    }

    draw.rounded_rectangle(
        (
            cta_box["x"],
            cta_box["y"],
            cta_box["x"] + cta_box["width"],
            cta_box["y"] + cta_box["height"]
        ),
        radius=0,
        fill="#59A3FF"
    )

    draw_auto_fit_text(
        draw,
        "Telegram",
        cta_box,
        50,
        TEXT_COLOR,
        bold=False,
        align="center",
        vertical="center"
    )

    # -------------------------------------------------
    # Subtitle
    # -------------------------------------------------

    draw_auto_fit_text(
        draw,
        "المجلس",
        {
            "x": 1522,
            "y": 587,
            "width": 280,
            "height": 83
        },
        7,
        TEXT_COLOR,
        bold=False,
        align="right",
        vertical="center"
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

    draw_auto_fit_text(
        draw,
        channel,
        {
            "x": 556,
            "y": 975,
            "width": 809,
            "height": 63
        },
        40,
        TEXT_COLOR,
        bold=False,
        align="center",
        vertical="top"
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

    draw_auto_fit_text(
        draw,
        episode,
        {
            "x": 58,
            "y": 581,
            "width": 245,
            "height": 96
        },
        60,
        TEXT_COLOR,
        bold=False,
        align="right",
        vertical="center"
    )

    # -------------------------------------------------
    # الشيخ عبد الكريم الكثيري حفظه الله
    # -------------------------------------------------

    draw_auto_fit_text(
        draw,
        "الشيخ عبد الكريم\nالكثيري حفظه الله",
        {
            "x": 1540,
            "y": 38,
            "width": 368,
            "height": 132
        },
        50,
        "#000000",
        bold=True,
        align="center",
        vertical="center"
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
