# -*- coding: utf-8 -*-

import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
import arabic_reshaper
from bidi.algorithm import get_display


# -----------------------------
# مسیرها (بدون دعوا با لینوکس)
# -----------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)

FONT_PATH = os.path.join(BASE_DIR, "fonts", "Vazirmatn-Regular.ttf")
OUTPUT_PDF = os.path.join(BASE_DIR, "afghanisstan.pdf")


# -----------------------------
# ثبت فونت فارسی
# -----------------------------
if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(f"Font not found: {FONT_PATH}")

pdfmetrics.registerFont(
    TTFont("Vazir", FONT_PATH)
)


# -----------------------------
# استایل‌ها
# -----------------------------
title_style = ParagraphStyle(
    name="Title",
    fontName="Vazir",
    fontSize=18,
    leading=22
)

section_style = ParagraphStyle(
    name="Section",
    fontName="Vazir",
    fontSize=14,
    leading=18
)

normal_style = ParagraphStyle(
    name="Normal",
    fontName="Vazir",
    fontSize=12,
    leading=16
)


# -----------------------------
# تابع اصلاح RTL
# -----------------------------
def fix_rtl(text: str) -> str:
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


# -----------------------------
# ساخت سند
# -----------------------------
doc = SimpleDocTemplate(OUTPUT_PDF, pagesize=A4)
elements = []

# عنوان
elements.append(
    Paragraph(
        fix_rtl("تاریخ افغانستان پس از جدایی از ایران"),
        title_style
    )
)
elements.append(Spacer(1, 0.3 * inch))


# -----------------------------
# محتوا
# -----------------------------
sections = {
    "۱) شکل‌گیری افغانستان مستقل (۱۷۴۷–۱۸۲۳)": """
پس از فروپاشی دولت صفویه و دوره آشوب در ایران، احمدشاه درانی در سال ۱۷۴۷ میلادی
حکومت مستقلی را پایه‌گذاری کرد که هسته اصلی افغانستان امروزی شد.
او قبایل پشتون را متحد کرد و قلمرو خود را گسترش داد.
""",

    "۲) بازی بزرگ و جنگ‌های انگلیس (۱۸۲۳–۱۹۱۹)": """
افغانستان به منطقه حائل میان بریتانیا و روسیه تزاری تبدیل شد.
سه جنگ میان افغانستان و بریتانیا رخ داد.
سیاست خارجی کشور تحت نفوذ بریتانیا بود.
""",

    "۳) استقلال کامل و اصلاحات (۱۹۱۹–۱۹۷۳)": """
پس از جنگ سوم، افغانستان استقلال کامل سیاست خارجی را به دست آورد.
اصلاحات آموزشی و اجتماعی آغاز شد اما با مقاومت سنتی‌ها مواجه گردید.
""",

    "۴) کودتا و دوره کمونیستی (۱۹۷۳–۱۹۷۹)": """
نظام پادشاهی سقوط کرد و حکومت کمونیستی روی کار آمد.
اصلاحات اجباری موجب شورش‌های گسترده شد.
""",

    "۵) اشغال شوروی (۱۹۷۹–۱۹۸۹)": """
ارتش شوروی وارد افغانستان شد.
جنگی ده‌ساله آغاز شد که خسارات انسانی و اقتصادی سنگینی به جا گذاشت.
""",

    "۶) جنگ داخلی مجاهدین (۱۹۸۹–۱۹۹۶)": """
پس از خروج شوروی، گروه‌های مجاهدین وارد جنگ داخلی شدند.
کابل به شدت آسیب دید.
""",

    "۷) حکومت اول طالبان (۱۹۹۶–۲۰۰۱)": """
طالبان قدرت را به دست گرفتند.
قوانین سخت‌گیرانه اعمال شد و کشور منزوی گردید.
""",

    "۸) مداخله آمریکا و جمهوری (۲۰۰۱–۲۰۲۱)": """
پس از حملات ۱۱ سپتامبر، طالبان سقوط کردند.
نظام جمهوری با حمایت بین‌المللی شکل گرفت اما مشکلات ساختاری ادامه داشت.
""",

    "۹) بازگشت طالبان (۲۰۲۱ تاکنون)": """
با خروج نیروهای آمریکایی، طالبان دوباره قدرت را به دست گرفتند.
افغانستان با بحران اقتصادی و اجتماعی مواجه است.
"""
}


# -----------------------------
# اضافه‌کردن به PDF
# -----------------------------
for title, content in sections.items():
    elements.append(Paragraph(fix_rtl(title), section_style))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(fix_rtl(content.strip()), normal_style))
    elements.append( Spacer (1, 0.4 * inch))


# -----------------------------
# ساخت نهایی PDF
# -----------------------------
doc.build(elements)

print("PDF با موفقیت ساخته شد:")
print(OUTPUT_PDF)
