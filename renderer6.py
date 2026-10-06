import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from style import STYLE


WIDTH = 1920
HEIGHT = 1080

WHITE_BOX_ALPHA = 110
BOX_CORNER_RADIUS = 25


def load_style_font(style_name, size):
    style = STYLE[style_name]
    return ImageFont.truetype(
        str(style["font"]),
        size
    )


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


def draw_transparent_box(canvas, box):
    overlay = Image.new(
        "RGBA",
        canvas.size,
        (0, 0, 0, 0)
    )

    overlay_draw = ImageDraw.Draw(overlay)

    x = box["x"]
    y = box["y"]
    width = box["width"]
    height = box["height"]

    overlay_draw.rounded_rectangle(
        (
            x,
            y,
            x + width,
            y + height
        ),
        radius=BOX_CORNER_RADIUS,
        fill=(255, 255, 255, WHITE_BOX_ALPHA)
    )

    canvas.alpha_composite(overlay)


def draw_auto_fit_text(
    draw,
    text,
    box,
    max_font_size,
    min_font_size,
    style_name,
    align="left",
    vertical="center",
    spacing=4
):
    x = box["x"]
    y = box["y"]
    width = box["width"]
    height = box["height"]

    style = STYLE[style_name]

    font_size = max_font_size

    while font_size >= min_font_size:
        font = load_style_font(
            style_name,
            font_size
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

    font = load_style_font(
        style_name,
        max(font_size, min_font_size)
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
        fill=style["color"],
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

    if data.get("include_logo", True):
        canvas.alpha_composite(
            logo,
            (19, 19),
        )

    # =========================================================
    # Bottom shared box
    # Telegram + Channel + المجلس + Episode + Speaker
    # =========================================================

    bottom_box = {
        "x": 33,
        "y": 960,
        "width": 1795,
        "height": 90
    }

    draw_transparent_box(
        canvas,
        bottom_box
    )

    draw = ImageDraw.Draw(canvas)

    # Telegram :
    draw_auto_fit_text(
        draw,
        "Telegram :",
        {
            "x": 52,
            "y": 970,
            "width": 211,
            "height": 55
        },
        max_font_size=50,
        min_font_size=15,
        style_name="telegram",
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
            "y": 970,
            "width": 516,
            "height": 55
        },
        max_font_size=40,
        min_font_size=10,
        style_name="channel",
        align="left",
        vertical="center"
    )

    # الشيخ عبد الكريم الكثيري حفظه الله
    draw_auto_fit_text(
        draw,
        "الشيخ عبد الكريم الكثيري حفظه الله",
        {
            "x": 779,
            "y": 970,
            "width": 776,
            "height": 55
        },
        max_font_size=40,
        min_font_size=15,
        style_name="sheikh",
        align="center",
        vertical="center"
    )

    # رقم المجلس
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
            "height": 55
        },
        max_font_size=50,
        min_font_size=15,
        style_name="episode",
        align="right",
        vertical="center"
    )

    # المجلس
    draw_auto_fit_text(
        draw,
        "المجلس",
        {
            "x": 1658,
            "y": 970,
            "width": 170,
            "height": 55
        },
        max_font_size=50,
        min_font_size=15,
        style_name="council",
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

    title_box = {
        "x": 779,
        "y": 58,
        "width": 1073,
        "height": 503
    }

    draw_transparent_box(
        canvas,
        title_box
    )

    draw = ImageDraw.Draw(canvas)

    draw_auto_fit_text(
        draw,
        title,
        title_box,
        max_font_size=60,
        min_font_size=15,
        style_name="title",
        align="center",
        vertical="center"
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
