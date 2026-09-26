```python
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
    vertical="center",
    spacing=4
):
    x = box["x"]
    y = box["y"]
    width = box["width"]
    height = box["height"]

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
        text_y = y + (height - text_height) / 2 - bbox[1]

    draw.multiline_text(
        (text_x, text_y),
        text,
        font=font,
        fill=fill,
        spacing=spacing,
        align=align
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
    """
    Automatically reduces the font size until the text
    fits completely inside the specified box.
    """

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
        text_y = y + height - text_height - bbox[1]
    else:
        text_y = y + (height - text_height) / 2 - bbox[1]

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
        print("Usage: python renderer1.py input.json")
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

    # --------------------------------------------------
    # Background
    # --------------------------------------------------

    download_image(
        data["background"],
        background_path
    )

    background = Image.open(background_path)

    canvas = fit_background(background)

    # --------------------------------------------------
    # Logo
    # --------------------------------------------------

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

    # --------------------------------------------------
    # : المجلس
    # Template:
    # x=473 y=665
    # width=439 height=230
    # font-size=149
    # center / center
    # --------------------------------------------------

    font = load_font(
        149,
        bold=True
    )

    draw_text_box(
        draw,
        ": المجلس",
        {
            "x": 473,
            "y": 665,
            "width": 439,
            "height": 230
        },
        font,
        "#000000",
        "center",
        "center"
    )

    # --------------------------------------------------
    # Telegram :
    # Template:
    # x=36 y=895
    # width=331 height=159
    # font-size=88
    # left / center
    # --------------------------------------------------

    font = load_font(
        88,
        bold=True
    )

    draw_text_box(
        draw,
        "Telegram :",
        {
            "x": 36,
            "y": 895,
            "width": 331,
            "height": 159
        },
        font,
        "#000000",
        "left",
        "center"
    )

    # --------------------------------------------------
    # Episode
    # Dynamic input + Auto Fit
    # Template:
    # x=169 y=739
    # width=238 height=81
    # font-size=50
    # center / center
    # --------------------------------------------------

    episode = str(
        data.get(
            "episode",
            "20"
        )
    )

    draw_auto_fit_text(
        draw,
        episode,
        {
            "x": 169,
            "y": 739,
            "width": 238,
            "height": 81
        },
        max_font_size=50,
        min_font_size=15,
        bold=True,
        fill="#000000",
        align="center",
        vertical="center"
    )

    # --------------------------------------------------
    # Title
    # Dynamic input + Auto Fit
    # Template:
    # x=67 y=169
    # width=845 height=418
    # font-size=99
    # center / center
    # --------------------------------------------------

    title = str(
        data.get(
            "title",
            "التِّبيان لجَرْدِ الكُتبِ و المُطوَّلَات"
        )
    )

    draw_auto_fit_text(
        draw,
        title,
        {
            "x": 67,
            "y": 169,
            "width": 845,
            "height": 418
        },
        max_font_size=99,
        min_font_size=20,
        bold=True,
        fill="#000000",
        align="center",
        vertical="center"
    )

    # --------------------------------------------------
    # Channel
    # Dynamic input + Auto Fit
    # Template:
    # x=367 y=932
    # width=670 height=83
    # font-size=45
    # left / center
    # --------------------------------------------------

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
            "x": 367,
            "y": 932,
            "width": 670,
            "height": 83
        },
        max_font_size=45,
        min_font_size=10,
        bold=False,
        fill="#000000",
        align="left",
        vertical="center"
    )

    # --------------------------------------------------
    # Sheikh name
    # Template:
    # x=1530 y=924
    # width=354 height=100
    # font-size=50
    # center / center
    # two lines
    # --------------------------------------------------

    font = load_font(
        50,
        bold=True
    )

    draw_text_box(
        draw,
        "الشيخ عبد الكريم\nالكثيري حفظه الله",
        {
            "x": 1530,
            "y": 924,
            "width": 354,
            "height": 100
        },
        font,
        "#000000",
        "center",
        "center",
        spacing=4
    )

    # --------------------------------------------------
    # Save
    # --------------------------------------------------

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
```
