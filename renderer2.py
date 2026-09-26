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
    bold=True,
    fill="#000000",
    align="center",
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
        print("Usage: python renderer2.py input.json")
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
    # المجلس - title Duplicate 5
    # Template:
    # x=1719 y=889
    # width=175 height=150
    # font-size=50
    # center / center
    # -------------------------------------------------

    draw_auto_fit_text(
        draw,
        "المجلس",
        {
            "x": 1719,
            "y": 889,
            "width": 175,
            "height": 150
        },
        max_font_size=50,
        min_font_size=15,
        bold=True,
        fill="#000000",
        align="center",
        vertical="center"
    )

    # -------------------------------------------------
    # Title
    # Template:
    # x=446 y=240
    # width=1029 height=601
    # font-size=152
    # center / center
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
            "x": 446,
            "y": 240,
            "width": 1029,
            "height": 601
        },
        max_font_size=152,
        min_font_size=20,
        bold=False,
        fill="#000000",
        align="center",
        vertical="center"
    )

    # -------------------------------------------------
    # Episode
    # Template:
    # x=1566 y=929
    # width=202 height=69
    # font-size=65
    # center / center
    # -------------------------------------------------

    episode = str(
        data.get(
            "episode",
            "50"
        )
    )

    draw_auto_fit_text(
        draw,
        episode,
        {
            "x": 1566,
            "y": 929,
            "width": 202,
            "height": 69
        },
        max_font_size=65,
        min_font_size=15,
        bold=True,
        fill="#000000",
        align="center",
        vertical="center"
    )

    # -------------------------------------------------
    # Channel
    # Template:
    # x=26 y=995
    # width=577 height=47
    # font-size=20
    # left / center
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
            "x": 26,
            "y": 995,
            "width": 577,
            "height": 47
        },
        max_font_size=20,
        min_font_size=8,
        bold=True,
        fill="#002030",
        align="left",
        vertical="center"
    )

    # -------------------------------------------------
    # Telegram
    # Template:
    # x=21 y=944
    # width=361 height=39
    # font-size=40
    # left / top
    # -------------------------------------------------

    draw_auto_fit_text(
        draw,
        "Telegram",
        {
            "x": 21,
            "y": 944,
            "width": 361,
            "height": 39
        },
        max_font_size=40,
        min_font_size=10,
        bold=True,
        fill="#002030",
        align="left",
        vertical="top"
    )

    # -------------------------------------------------
    # الشيخ عبد الكريم الكثيري حفظه الله
    # Template:
    # x=768 y=914
    # width=725 height=100
    # font-size=50
    # center / center
    # -------------------------------------------------

    draw_auto_fit_text(
        draw,
        "الشيخ عبد الكريم الكثيري حفظه الله",
        {
            "x": 768,
            "y": 914,
            "width": 725,
            "height": 100
        },
        max_font_size=50,
        min_font_size=15,
        bold=True,
        fill="#000000",
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
