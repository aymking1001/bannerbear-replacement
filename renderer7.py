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
    style_name,
    align="left",
    vertical="center",
    min_font_size=1,
    spacing=0
):
    x = box["x"]
    y = box["y"]
    width = box["width"]
    height = box["height"]

    style = STYLE[style_name]

    text = str(text)

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
            align=align,
            spacing=spacing
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
        align=align,
        spacing=spacing
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center horizontally
    text_x = (
        x
        + (width - text_width) / 2
    )

    # Center vertically
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
        align="center",
        spacing=spacing
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

    if data.get("include_logo", True):
        canvas.alpha_composite(
            logo,
            (19, 19),
        )

    draw = ImageDraw.Draw(canvas)

    # -------------------------------------------------
    # Title
    # -------------------------------------------------

    title = str(
        data.get(
            "title",
            "التِّبيان لجَرْدِ الكُتبِ والمُطوَّلَات"
        )
    )

    title_box = {
        "x": 592,
        "y": 419,
        "width": 736,
        "height": 418
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
        50,
        "title",
        min_font_size=1
    )

    # -------------------------------------------------
    # CTA - Telegram
    # -------------------------------------------------

    cta_box = {
        "x": 698,
        "y": 911,
        "width": 525,
        "height": 64
    }

    draw_transparent_box(
        canvas,
        cta_box
    )

    draw = ImageDraw.Draw(canvas)

    draw_auto_fit_text(
        draw,
        "Telegram",
        cta_box,
        50,
        "telegram"
    )

    # -------------------------------------------------
    # المجلس
    # -------------------------------------------------

    subtitle_box = {
        "x": 1522,
        "y": 587,
        "width": 280,
        "height": 83
    }

    draw_transparent_box(
        canvas,
        subtitle_box
    )

    draw = ImageDraw.Draw(canvas)

    draw_auto_fit_text(
        draw,
        "المجلس",
        subtitle_box,
        50,
        "council",
        min_font_size=10
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

    channel_box = {
        "x": 556,
        "y": 975,
        "width": 809,
        "height": 63
    }

    draw_transparent_box(
        canvas,
        channel_box
    )

    draw = ImageDraw.Draw(canvas)

    draw_auto_fit_text(
        draw,
        channel,
        channel_box,
        40,
        "channel"
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

    episode_box = {
        "x": 58,
        "y": 581,
        "width": 245,
        "height": 96
    }

    draw_transparent_box(
        canvas,
        episode_box
    )

    draw = ImageDraw.Draw(canvas)

    draw_auto_fit_text(
        draw,
        episode,
        episode_box,
        60,
        "episode"
    )

    # -------------------------------------------------
    # الشيخ عبد الكريم الكثيري حفظه الله
    # -------------------------------------------------

    speaker_box = {
        "x": 1540,
        "y": 38,
        "width": 368,
        "height": 132
    }

    draw_transparent_box(
        canvas,
        speaker_box
    )

    draw = ImageDraw.Draw(canvas)

    draw_auto_fit_text(
        draw,
        "الشيخ عبد الكريم\nالكثيري حفظه الله",
        speaker_box,
        50,
        "sheikh"
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
