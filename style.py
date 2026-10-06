from pathlib import Path

# ============================================================
# المسار الرئيسي للمشروع
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

FONTS_DIR = BASE_DIR / "fonts"

# ============================================================
# الخطوط
# ============================================================

# ------------------------------------------------------------
# العنوان
# خط الثلث الجلي — Jali Thuluth
# ------------------------------------------------------------
TITLE_FONT = FONTS_DIR / "JaliThuluth.ttf"

# ------------------------------------------------------------
# كلمة "المجلس"
# خط النسخ — Naskh Arabic
# ------------------------------------------------------------
COUNCIL_FONT = FONTS_DIR / "NaskhArabic.ttf"

# ------------------------------------------------------------
# رقم المجلس / رقم الحلقة
# يبقى كما هو في الرندرات الحالية
# ------------------------------------------------------------
EPISODE_FONT = Path(
    "/usr/share/fonts/truetype/dejavu/"
    "DejaVuSans-Bold.ttf"
)

# ------------------------------------------------------------
# اسم الشيخ
# خط الديواني الجلي — Jali Diwani
# ------------------------------------------------------------
SHEIKH_FONT = FONTS_DIR / "JaliDiwani.ttf"

# ------------------------------------------------------------
# كلمة Telegram
# تبقى كما هي في الرندرات الحالية
# ------------------------------------------------------------
TELEGRAM_FONT = Path(
    "/usr/share/fonts/truetype/dejavu/"
    "DejaVuSans-Bold.ttf"
)

# ------------------------------------------------------------
# الرابط
# يبقى كما هو في الرندرات الحالية
# ------------------------------------------------------------
CHANNEL_FONT = Path(
    "/usr/share/fonts/truetype/dejavu/"
    "DejaVuSans.ttf"
)

# ============================================================
# الألوان
# ============================================================

TITLE_COLOR = "#000000"
COUNCIL_COLOR = "#000000"
EPISODE_COLOR = "#000000"
SHEIKH_COLOR = "#000000"
TELEGRAM_COLOR = "#000000"
CHANNEL_COLOR = "#000000"

# ============================================================
# إعدادات الخط العريض
# ============================================================

TITLE_BOLD = False
COUNCIL_BOLD = False
EPISODE_BOLD = True
SHEIKH_BOLD = False
TELEGRAM_BOLD = True
CHANNEL_BOLD = False

# ============================================================
# إعدادات جميع العناصر
# ============================================================

STYLE = {
    "title": {
        "font": TITLE_FONT,
        "color": TITLE_COLOR,
        "bold": TITLE_BOLD,
    },
    "council": {
        "font": COUNCIL_FONT,
        "color": COUNCIL_COLOR,
        "bold": COUNCIL_BOLD,
    },
    "episode": {
        "font": EPISODE_FONT,
        "color": EPISODE_COLOR,
        "bold": EPISODE_BOLD,
    },
    "sheikh": {
        "font": SHEIKH_FONT,
        "color": SHEIKH_COLOR,
        "bold": SHEIKH_BOLD,
    },
    "telegram": {
        "font": TELEGRAM_FONT,
        "color": TELEGRAM_COLOR,
        "bold": TELEGRAM_BOLD,
    },
    "channel": {
        "font": CHANNEL_FONT,
        "color": CHANNEL_COLOR,
        "bold": CHANNEL_BOLD,
    },
}
