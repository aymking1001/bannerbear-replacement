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
    min_font_size,
    bold=False,
    fill="#000000",
    align="left",
    vertical="center",
    spacing=4
):
    x = box["x"]
    y = box["y"]
    width = box["width"]
    height = box["height"]

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
            spacing=spacing,
            align=align
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
        spacing=spacing,
        align=align
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
        text_y = (
            y
            + height
            - text_height
            - bbox[1]
        )

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
        spacing=spacing,
        align=align
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

    # Telegram :
    draw_auto_fit_text(
        draw,
        "Telegram :",
        {
            "x": 52,
            "y": 962,
            "width": 211,
            "height": 77
        },
        max_font_size=50,
        min_font_size=15,
        bold=True,
        fill="#000000",
        align="left",
        vertical="center"
    )

    # Channel
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
            "x": 263,
            "y": 978,
            "width": 516,
            "height": 45
        },
        max_font_size=40,
        min_font_size=10,
        bold=True,
        fill="#000000",
        align="left",
        vertical="top"
    )

    # المجلس
    draw_auto_fit_text(
        draw,
        "المجلس",
        {
            "x": 1658,
            "y": 975,
            "width": 170,
            "height": 50
        },
        max_font_size=50,
        min_font_size=15,
        bold=True,
        fill="#303030",
        align="right",
        vertical="top"
    )

    # Episode
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
            "x": 1544,
            "y": 970,
            "width": 114,
            "height": 61
        },
        max_font_size=50,
        min_font_size=15,
        bold=True,
        fill="#262626",
        align="right",
        vertical="center"
    )

    # Title
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
            "x": 779,
            "y": 58,
            "width": 1073,
            "height": 503
        },
        max_font_size=60,
        min_font_size=15,
        bold=True,
        fill="#282828",
        align="center",
        vertical="center"
    )

    # الشيخ عبد الكريم الكثيري حفظه الله
    draw_auto_fit_text(
        draw,
        "الشيخ عبد الكريم الكثيري حفظه الله",
        {
            "x": 779,
            "y": 965,
            "width": 776,
            "height": 71
        },
        max_font_size=50,
        min_font_size=15,
        bold=True,
        fill="#000000",
        align="center",
        vertical="top"
    )

    # Save
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
