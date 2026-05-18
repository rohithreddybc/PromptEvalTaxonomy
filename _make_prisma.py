"""
Generate a PRISMA 2020 flowchart PNG in the same visual format as
prisma_flowchart_OLD_backup.png, but with the updated Claude Code
content/counts for all five rounds, ending with 152 papers.

Output:
  prisma_flowchart.png

This script intentionally uses Pillow instead of Matplotlib so the geometry,
rounded phase labels, box outlines, arrows, typography, and 1024 x 1536 canvas
match the old backup-style figure more closely.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---------------------------------------------------------------------------
# Content from the Claude Code / all-rounds PRISMA version
# ---------------------------------------------------------------------------
CONTENT = {
    "identified": [
        "Records identified from:",
        "- Round 0 (primary search, 6 databases): n = 2,847",
        "- arXiv, ACM DL, IEEE Xplore, Semantic Scholar, Scopus, Web of Science",
        "- Rounds 1-4 (targeted expansions, same databases): n = 450",
        "Total records identified: n = 3,297",
    ],
    "screened": [
        "Records screened by title / abstract",
        "Round 0: n = 2,847",
        "Rounds 1-4 (targeted queries): went directly to full-text review",
    ],
    "title_excluded": [
        "Records excluded",
        "at title/abstract",
        "(round 0 only): n = 2,435",
    ],
    "full_text": [
        "Reports assessed for eligibility",
        "(full-text review)",
        "Round 0: 412    Rounds 1-4: 118 + 74 + 212 + 46 = 450",
        "Total full-text reviewed: n = 862",
    ],
    "full_text_excluded": [
        "Reports excluded at full-text",
        "(n = 732):",
        "- Prompting as tool: 181",
        "- Domain-specific: 64",
        "- No full text: 24",
        "- Non-English: 14",
        "- Venue filter (Rnd 0): 71",
        "- Expansion rounds: 377",
        "- Duplicate (Rnd 0 & Rnd 1): 1",
    ],
    "passed": [
        "Reports passing full-text review",
        "Round 0: 57    Rounds 1-4: 73",
        "Total: n = 130",
    ],
    "venue_filter": [
        "Round-0 venue filter",
        "(peer-review / tier):",
        "Excluded: 71    Retained: 57",
        "Rounds 1-4: venue-filtered at intake; all 73 retained",
    ],
    "included": [
        "Total reports for inclusion",
        "Round 0: venue-filtered (57) + citation search (22) = 79",
        "Rounds 1-4 targeted expansions: 20 + 11 + 35 + 7 = 73",
        "Total eligible: n = 152",
    ],
    "citation": [
        "Round-0 citation search",
        "(backward / forward): +22 papers",
        "Rounds 1-4 additions: +73 papers",
    ],
    "final": [
        "FINAL CORPUS",
        "n = 152 papers",
    ],
}

# ---------------------------------------------------------------------------
# Canvas and fonts
# ---------------------------------------------------------------------------
W, H = 1024, 1536
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

FONT_DIR = Path(r"C:\Windows\Fonts")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    path = FONT_DIR / name
    if path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.truetype("DejaVuSans.ttf", size)


F_TITLE = font("arialbd.ttf", 40)
F_STAGE = font("arialbd.ttf", 28)
F_BOLD_28 = font("arialbd.ttf", 28)
F_BOLD_26 = font("arialbd.ttf", 26)
F_BOLD_24 = font("arialbd.ttf", 24)
F_BOLD_23 = font("arialbd.ttf", 23)
F_BOLD_22 = font("arialbd.ttf", 22)
F_BOLD_21 = font("arialbd.ttf", 21)
F_REG_24 = font("arial.ttf", 24)
F_REG_22 = font("arial.ttf", 22)
F_REG_20 = font("arial.ttf", 20)
F_REG_19 = font("arial.ttf", 19)
F_REG_18 = font("arial.ttf", 18)
F_REG_17 = font("arial.ttf", 17)
F_FINAL = font("arialbd.ttf", 31)

BLUE = (24, 67, 101)
PURPLE = (82, 57, 100)
GREEN = (43, 96, 50)
RED = (130, 30, 24)
BLACK = (18, 18, 18)
WHITE = (255, 255, 255)

# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def text_size(text, f):
    box = d.textbbox((0, 0), text, font=f)
    return box[2] - box[0], box[3] - box[1]


def gradient_rect(x0, y0, x1, y1, c1, c2, radius=10, outline=None, width=3):
    w, h = x1 - x0, y1 - y0
    grad = Image.new("RGB", (w, h), c1)
    gd = ImageDraw.Draw(grad)

    for x in range(w):
        t = x / max(1, w - 1)
        c = tuple(int(c1[i] * (1 - t) + c2[i] * t) for i in range(3))
        gd.line([(x, 0), (x, h)], fill=c)

    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=255)
    img.paste(grad, (x0, y0), mask)

    if outline:
        d.rounded_rectangle((x0, y0, x1, y1), radius=radius, outline=outline, width=width)


def box(x0, y0, x1, y1, outline, width=3, radius=7):
    d.rounded_rectangle((x0, y0, x1, y1), radius=radius, fill="white", outline=outline, width=width)


def arrow(start, end, color=BLACK, width=3, head=16):
    x0, y0 = start
    x1, y1 = end
    d.line((x0, y0, x1, y1), fill=color, width=width)

    if abs(x1 - x0) >= abs(y1 - y0):
        s = 1 if x1 >= x0 else -1
        pts = [(x1, y1), (x1 - s * head, y1 - head // 2), (x1 - s * head, y1 + head // 2)]
    else:
        s = 1 if y1 >= y0 else -1
        pts = [(x1, y1), (x1 - head // 2, y1 - s * head), (x1 + head // 2, y1 - s * head)]

    d.polygon(pts, fill=color)


def wrap_lines(text, f, max_w):
    lines = []

    for raw in text.split("\n"):
        words = raw.split()
        if not words:
            lines.append("")
            continue

        cur = words[0]
        for word in words[1:]:
            candidate = cur + " " + word
            if text_size(candidate, f)[0] <= max_w:
                cur = candidate
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)

    return lines


def draw_center_block(rect, rows, fonts, pad=18, line_gap=4, fill=BLACK):
    x0, y0, x1, y1 = rect
    max_w = x1 - x0 - 2 * pad

    prepared = []
    for text, f in zip(rows, fonts):
        for line in wrap_lines(text, f, max_w):
            prepared.append((line, f))

    total_h = sum(text_size(line, f)[1] + line_gap for line, f in prepared) - line_gap
    y = y0 + ((y1 - y0) - total_h) / 2

    for line, f in prepared:
        tw, th = text_size(line, f)
        d.text((x0 + (x1 - x0 - tw) / 2, y), line, font=f, fill=fill)
        y += th + line_gap


def draw_left_block(rect, rows, fonts, pad=22, line_gap=7, fill=BLACK):
    x0, y0, x1, y1 = rect
    max_w = x1 - x0 - 2 * pad

    prepared = []
    for text, f in zip(rows, fonts):
        for line in wrap_lines(text, f, max_w):
            prepared.append((line, f))

    total_h = sum(text_size(line, f)[1] + line_gap for line, f in prepared) - line_gap
    y = y0 + ((y1 - y0) - total_h) / 2

    for line, f in prepared:
        d.text((x0 + pad, y), line, font=f, fill=fill)
        y += text_size(line, f)[1] + line_gap


def draw_stage_label(rect, label, top_color, bottom_color, outline):
    x0, y0, x1, y1 = rect

    shadow = Image.new("RGBA", (x1 - x0 + 10, y1 - y0 + 10), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((3, 3, x1 - x0 + 3, y1 - y0 + 3), radius=10, fill=(0, 0, 0, 25))
    shadow = shadow.filter(ImageFilter.GaussianBlur(2))
    img.paste(shadow, (x0 - 3, y0 - 3), shadow)

    gradient_rect(x0, y0, x1, y1, top_color, bottom_color, radius=10, outline=outline)

    tw, th = text_size(label, F_STAGE)
    label_img = Image.new("RGBA", (tw + 8, th + 8), (0, 0, 0, 0))
    td = ImageDraw.Draw(label_img)
    td.text((4, 4), label, font=F_STAGE, fill=BLACK)
    rotated = label_img.rotate(90, expand=True)
    img.paste(rotated, (x0 + (x1 - x0 - rotated.width) // 2, y0 + (y1 - y0 - rotated.height) // 2), rotated)

# ---------------------------------------------------------------------------
# Fixed geometry copied from the old backup format
# ---------------------------------------------------------------------------

title = "PRISMA 2020 Screening Flowchart"
tw, _ = text_size(title, F_TITLE)
d.text(((W - tw) / 2, 28), title, font=F_TITLE, fill="black")

draw_stage_label((70, 88, 132, 432), "IDENTIFICATION", (218, 237, 254), (190, 216, 240), BLUE)
draw_stage_label((70, 456, 132, 816), "SCREENING", (218, 237, 254), (190, 216, 240), BLUE)
draw_stage_label((70, 837, 132, 1077), "ELIGIBILITY", (224, 213, 242), (202, 192, 224), PURPLE)
draw_stage_label((70, 1098, 132, 1409), "INCLUDED", (226, 241, 222), (205, 230, 202), GREEN)

b1 = (170, 93, 655, 436)
b2 = (170, 491, 655, 604)
b3 = (170, 669, 613, 797)
b4 = (195, 868, 594, 994)
b5 = (195, 1072, 671, 1216)
b6 = (195, 1293, 646, 1405)
r2 = (722, 498, 959, 617)
r3 = (670, 663, 994, 842)
r4 = (670, 885, 994, 1007)
r5 = (732, 1103, 970, 1219)

for rect, color in [(b1, BLUE), (b2, BLUE), (b3, PURPLE), (b4, PURPLE), (b5, GREEN)]:
    box(*rect, outline=color)

for rect, color in [(r2, RED), (r3, RED), (r4, RED), (r5, GREEN)]:
    box(*rect, outline=color)

gradient_rect(*b6, (38, 98, 46), (30, 111, 46), radius=7)

cx = 411
for start, end in [
    ((cx, 436), (cx, 488)),
    ((cx, 604), (cx, 666)),
    ((cx, 797), (cx, 865)),
    ((cx, 994), (cx, 1069)),
    ((cx, 1216), (cx, 1290)),
    ((655, 548), (719, 548)),
    ((613, 729), (667, 729)),
    ((594, 935), (667, 935)),
    ((671, 1152), (729, 1152)),
]:
    arrow(start, end)

# ---------------------------------------------------------------------------
# Text placement
# ---------------------------------------------------------------------------

draw_left_block(b1, CONTENT["identified"], [F_BOLD_28, F_REG_24, F_REG_24, F_REG_24, F_BOLD_26])
draw_center_block(b2, CONTENT["screened"], [F_BOLD_23, F_REG_22, F_REG_18])
draw_center_block(r2, CONTENT["title_excluded"], [F_BOLD_24, F_REG_22, F_REG_20])
draw_center_block(b3, CONTENT["full_text"], [F_BOLD_23, F_REG_22, F_REG_17, F_REG_19])
draw_center_block(
    r3,
    CONTENT["full_text_excluded"],
    [F_BOLD_21, F_BOLD_21, F_REG_19, F_REG_19, F_REG_19, F_REG_19, F_REG_19, F_REG_19],
    line_gap=2,
)
draw_center_block(b4, CONTENT["passed"], [F_BOLD_24, F_REG_22, F_REG_20])
draw_center_block(r4, CONTENT["venue_filter"], [F_BOLD_21, F_REG_19, F_REG_20, F_REG_18])
draw_center_block(b5, CONTENT["included"], [F_BOLD_24, F_REG_19, F_REG_19, F_BOLD_22])
draw_center_block(r5, CONTENT["citation"], [F_REG_18, F_REG_18, F_REG_18], line_gap=3)
draw_center_block(b6, CONTENT["final"], [F_FINAL, F_FINAL], fill=WHITE, line_gap=8)

# ---------------------------------------------------------------------------
# Save beside this script
# ---------------------------------------------------------------------------

out_path = Path(__file__).resolve().with_name("prisma_flowchart.png")
img.save(out_path, dpi=(300, 300))
print(f"wrote {out_path}")
print(f"  size: {out_path.stat().st_size} bytes")
print("  dimensions: 1024 x 1536 px; dpi: 300")
