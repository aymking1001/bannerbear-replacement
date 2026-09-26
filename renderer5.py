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
    spacing=4,
):
    x = box["x"]
    y = box["y"]
    width = box["width"]
    height = box["height"]

    font_size = max_font_size

    while font_size >= min_font_size:
        font = load_font(
            font_size,
            bold=bold,
        )

        bbox = draw.multiline_textbbox(
            (0, 0),
            text,
            font=font,
            spacing=spacing,
            align=align,
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
        bold=bold,
    )

    bbox = draw.multiline_textbbox(
        (0, 0),
        text,
        font=font,
        spacing=spacing,
        align=align,
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
        align=align,
    )


def main():
    if len(sys.argv) != 2:
        print("Usage: python renderer5.py input.json")
        sys.exit(1)

    input_file = Path(sys.argv[1])

    with open(
        input_file,
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)

    work_dir = Path("work")
    work_dir.mkdir(exist_ok=True)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    background_path = work_dir / "background"
    logo_path = work_dir / "logo"

    # 1. Background
    download_image(
        data["background"],
        background_path,
    )

    background = Image.open(background_path)
    canvas = fit_background(background)

    # 2. Logo
    download_image(
        data["logo"],
        logo_path,
    )

    logo = Image.open(
        logo_path
    ).convert("RGBA")

    logo = logo.resize(
        (150, 150),
        Image.Resampling.LANCZOS,
    )

    # Template 5 logo is circular
    mask = Image.new(
        "L",
        (150, 150),
        0,
    )

    mask_draw = ImageDraw.Draw(mask)

    mask_draw.ellipse(
        (0, 0, 149, 149),
        fill=255,
    )

    logo.putalpha(mask)

    canvas = canvas.convert("RGBA")

    canvas.alpha_composite(
        logo,
        (19, 19),
    )

    draw = ImageDraw.Draw(canvas)

    # Template 5 color
    TEXT_COLOR = "#3c3d72"

    # 3. Fixed subtitle: المجلس
    draw_auto_fit_text(
        draw,
        "المجلس",
        {
            "x": 1657,
            "y": 761,
            "width": 219,
            "height": 206,
        },
        max_font_size=37,
        min_font_size=15,
        bold=True,
        fill=TEXT_COLOR,
        align="left",
        vertical="center",
    )

    # 4. Episode
    episode = str(
        data.get(
            "episode",
            "10",
        )
    )

    draw_auto_fit_text(
        draw,
        episode,
        {
            "x": 1695,
            "y": 967,
            "width": 142,
            "height": 93,
        },
        max_font_size=50,
        min_font_size=15,
        bold=True,
        fill=TEXT_COLOR,
        align="center",
        vertical="center",
    )

    # 5. Title
    title = str(
        data.get(
            "title",
            "التِّبيان لجَرْدِ الكُتبِ والمُطوَّلَات",
        )
    )

    draw_auto_fit_text(
        draw,
        title,
        {
            "x": 473,
            "y": 626,
            "width": 974,
            "height": 476,
        },
        max_font_size=48,
        min_font_size=15,
        bold=True,
        fill=TEXT_COLOR,
        align="center",
        vertical="center",
    )

    # 6. Fixed Telegram text
    draw_auto_fit_text(
        draw,
        "Telegram",
        {
            "x": 40,
            "y": 910,
            "width": 248,
            "height": 57,
        },
        max_font_size=45,
        min_font_size=15,
        bold=True,
        fill=TEXT_COLOR,
        align="left",
        vertical="center",
    )

    # 7. Channel
    channel = str(
        data.get(
            "channel",
            "https://t.me/qatufwdurar",
        )
    )

    draw_auto_fit_text(
        draw,
        channel,
        {
            "x": 33,
            "y": 1004,
            "width": 375,
            "height": 46,
        },
        max_font_size=18,
        min_font_size=8,
        bold=False,
        fill=TEXT_COLOR,
        align="left",
        vertical="center",
    )

    # 8. Fixed speaker name
    draw_auto_fit_text(
        draw,
        "الشيخ عبد الكريم الكثيري حفظه الله",
        {
            "x": 384,
            "y": 63,
            "width": 1152,
            "height": 63,
        },
        max_font_size=50,
        min_font_size=15,
        bold=True,
        fill="#000000",
        align="center",
        vertical="center",
    )

    # 9. Save
    output_file = output_dir / "output.png"

    canvas.convert("RGB").save(
        output_file,
        "PNG",
    )

    print(
        f"Image created: {output_file}"
    )


if __name__ == "__main__":
    main()
