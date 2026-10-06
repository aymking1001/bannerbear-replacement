from pathlib import Path

# ============================================================

# المسار الرئيسي للمشروع

# ============================================================

BASE_DIR = Path(**file**).resolve().parent

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

EPISODE_FONT = (
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

TELEGRAM_FONT = (
"/usr/share/fonts/truetype/dejavu/"
"DejaVuSans-Bold.ttf"
)

# ------------------------------------------------------------

# الرابط

# يبقى كما هو في الرندرات الحالية

# ------------------------------------------------------------

CHANNEL_FONT = (
"/usr/share/fonts/truetype/dejavu/"
"DejaVuSans.ttf"
)

# ============================================================

# الألوان

# ============================================================

# العنوان

TITLE_COLOR = "#000000"

# كلمة المجلس

COUNCIL_COLOR = "#000000"

# رقم المجلس / رقم الحلقة

EPISODE_COLOR = "#000000"

# اسم الشيخ

SHEIKH_COLOR = "#000000"

# كلمة Telegram

TELEGRAM_COLOR = "#000000"

# الرابط

CHANNEL_COLOR = "#000000"

# ============================================================

# إعدادات الخط العريض

# ============================================================

# العنوان

TITLE_BOLD = False

# المجلس

COUNCIL_BOLD = False

# رقم المجلس / رقم الحلقة

EPISODE_BOLD = True

# اسم الشيخ

SHEIKH_BOLD = False

# Telegram

TELEGRAM_BOLD = True

# الرابط

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
