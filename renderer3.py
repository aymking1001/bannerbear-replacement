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
    x = box["x"]
    y = box["y"]
    width = box["width"]
    height = box["height"]

    overlay = Image.new(
        "RGBA",
        canvas.size,
        (0, 0, 0, 0)
    )

    overlay_draw = ImageDraw.Draw(
        overlay,
        "RGBA"
    )

    overlay_draw.rounded_rectangle(
        (
            x,
            y,
            x + width,
            y + height
        ),
        radius=BOX_CORNER_RADIUS,
        fill=(
            255,
            255,
            255,
            WHITE_BOX_ALPHA
        )
    )

    canvas.alpha_composite(
        overlay
    )


def draw_auto_fit_text(
    draw,
    text,
    box,
    max_font_size,
    min_font_size,
    style_name,
    align="center",
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
        fill=style["color"],
        spacing=spacing,
        align=align
    )


def main():

    if len(sys.argv) != 2:
        print("Usage: python renderer3.py input.json")
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

    if data.get("include_logo", True):
        canvas.alpha_composite(
            logo,
            (19, 19)
        )

    draw = ImageDraw.Draw(
        canvas,
        "RGBA"
    )

    # -------------------------------------------------
    # Title
    # Template:
    # x=377 y=55
    # width=1166 height=364
    # font-size=50
    # center / center
    # -------------------------------------------------

    title = str(
        data.get(
            "title",
            "التِّبيان لجَرْدِ الكُتبِ والمُطوَّلَات"
        )
    )

    title_box = {
        "x": 377,
        "y": 55,
        "width": 1166,
        "height": 364
    }

    draw_transparent_box(
        canvas,
        title_box
    )

    draw_auto_fit_text(
        draw,
        title,
        title_box,
        max_font_size=50,
        min_font_size=15,
        style_name="title",
        align="center",
        vertical="center"
    )

    # -------------------------------------------------
    # Telegram
    # Template:
    # x=169 y=883
    # width=150 height=40
    # font-size=50
    # left / center
    # -------------------------------------------------

    telegram_box = {
        "x": 169,
        "y": 883,
        "width": 150,
        "height": 40
    }

    draw_transparent_box(
        canvas,
        telegram_box
    )

    draw_auto_fit_text(
        draw,
        "Telegram",
        telegram_box,
        max_font_size=50,
        min_font_size=10,
        style_name="telegram",
        align="left",
        vertical="center"
    )

    # -------------------------------------------------
    # Channel
    # Template:
    # x=169 y=990
    # width=337 height=44
    # font-size=50
    # center / center
    # -------------------------------------------------

    channel = str(
        data.get(
            "channel",
            "https://t.me/qatufwdurar"
        )
    )

    channel_box = {
        "x": 169,
        "y": 990,
        "width": 337,
        "height": 44
    }

    draw_transparent_box(
        canvas,
        channel_box
    )

    draw_auto_fit_text(
        draw,
        channel,
        channel_box,
        max_font_size=50,
        min_font_size=10,
        style_name="channel",
        align="center",
        vertical="center"
    )

    # -------------------------------------------------
    # Episode
    # Template:
    # x=1543 y=992
    # width=208 height=40
    # font-size=50
    # center / center
    # -------------------------------------------------

    episode = str(
        data.get(
            "episode",
            "20"
        )
    )

    episode_box = {
        "x": 1543,
        "y": 992,
        "width": 208,
        "height": 40
    }

    draw_transparent_box(
        canvas,
        episode_box
    )

    draw_auto_fit_text(
        draw,
        episode,
        episode_box,
        max_font_size=50,
        min_font_size=10,
        style_name="episode",
        align="center",
        vertical="center"
    )

    # -------------------------------------------------
    # المجلس
    # Template:
    # x=1543 y=863
    # width=223 height=79
    # font-size=50
    # center / center
    # -------------------------------------------------

    council_box = {
        "x": 1543,
        "y": 863,
        "width": 223,
        "height": 79
    }

    draw_transparent_box(
        canvas,
        council_box
    )

    draw_auto_fit_text(
        draw,
        "المجلس",
        council_box,
        max_font_size=50,
        min_font_size=10,
        style_name="council",
        align="center",
        vertical="center"
    )

    # -------------------------------------------------
    # الشيخ عبد الكريم الكثيري حفظه الله
    # Template:
    # x=677 y=922
    # width=668 height=51
    # font-size=50
    # center / bottom
    # -------------------------------------------------

    sheikh_box = {
        "x": 677,
        "y": 922,
        "width": 668,
        "height": 51
    }

    draw_transparent_box(
        canvas,
        sheikh_box
    )

    draw_auto_fit_text(
        draw,
        "الشيخ عبد الكريم الكثيري حفظه الله",
        sheikh_box,
        max_font_size=50,
        min_font_size=10,
        style_name="sheikh",
        align="center",
        vertical="bottom"
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
