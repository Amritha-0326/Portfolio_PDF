from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

pdfmetrics.registerFont(
    TTFont("Jost", os.path.join(BASE_DIR, "fonts", "Jost-Regular.ttf"))
)
pdfmetrics.registerFont(
    TTFont("Jost-Bold", os.path.join(BASE_DIR, "fonts", "Jost-Bold.ttf"))
)

# ---------- COLORS ----------
PRIMARY = HexColor("#4C5C68")
ACCENT = HexColor("#B6A58D")
CTA = HexColor("#C37052")
SOFT_GREEN = HexColor("#B8CA93")
CARD_BG = HexColor("#F7F6F4")

# ---------- PAGE SETUP ----------
file_name = "Amritha_Portfolio.pdf"
c = canvas.Canvas(file_name, pagesize=A4)
width, height = A4
margin = 50

# ---------- HEADER ----------
c.setFillColor(SOFT_GREEN)
c.rect(0, height - 240, width, 240, fill=1, stroke=0)

# Profile Image Placeholder
c.setFillColor(white)
c.circle(margin + 40, height - 120, 35, fill=1)
c.setFillColor(PRIMARY)
c.setFont("Jost", 8)
c.drawCentredString(margin + 40, height - 125, "Profile")

# Name
c.setFont("Jost-Bold", 22)
c.drawString(margin + 100, height - 95, "Amritha Preetha Anil")

# Role
c.setFont("Jost", 12)
c.drawString(
    margin + 100,
    height - 125,
    "UX Designer solving complex problems with simple interactions"
)

y = height - 280

# ---------- PROFESSIONAL OVERVIEW ----------
c.setFillColor(PRIMARY)
c.setFont("Jost-Bold", 15)
c.drawString(margin, y, "Professional Overview")

y -= 22
c.setFont("Jost", 11)
overview = (
    "I’m just starting out as a UX designer, but I’m already passionate about turning "
    "user needs into intuitive, meaningful experiences. I bring curiosity, attention "
    "to detail, and a research-driven mindset to every project."
)
c.drawString(margin, y, overview)

y -= 55

# ---------- SKILLS ----------
c.setFont("Jost-Bold", 14)
c.drawString(margin, y, "Core Skills")
y -= 28

skills = ["Research", "UI Design", "Prototyping"]
card_w = 150
gap = 20

for i, skill in enumerate(skills):
    x = margin + i * (card_w + gap)
    c.setFillColor(ACCENT)
    c.roundRect(x, y - 42, card_w, 42, 10, fill=1, stroke=0)

    c.setFillColor(PRIMARY)
    c.setFont("Jost-Bold", 11)
    c.drawCentredString(x + card_w / 2, y - 27, skill)

y -= 80

# ---------- CERTIFICATES (BOXED LIKE PORTFOLIO) ----------
c.setFont("Jost-Bold", 14)
c.setFillColor(PRIMARY)
c.drawString(margin, y, "Certificates & Achievements")
y -= 30

certificates = [
    ("Foundations of UX Design", "Google Career Certificate · 2023"),
    ("UX Design Process", "Google Career Certificate · 2023"),
    ("UX Research & Early Testing", "Google Career Certificate · 2023"),
    ("Unit Testing in React.js", "Coursera · 2023"),
    ("React Basics", "Meta · In Progress")
]

box_w = 240
box_h = 75
gap_x = 20
gap_y = 20

start_x = margin
x = start_x

for i, (title, subtitle) in enumerate(certificates):
    if i % 2 == 0 and i != 0:
        x = start_x
        y -= box_h + gap_y

    c.setFillColor(CARD_BG)
    c.roundRect(x, y - box_h, box_w, box_h, 12, fill=1, stroke=0)

    c.setFillColor(PRIMARY)
    c.setFont("Jost-Bold", 11)
    c.drawString(x + 15, y - 28, title)

    c.setFont("Jost", 9.5)
    c.drawString(x + 15, y - 48, subtitle)

    x += box_w + gap_x

y -= 110

# ---------- PROJECTS ----------
c.setFont("Jost-Bold", 14)
c.drawString(margin, y, "Fun Projects & Learning")
y -= 28

projects = [
    "Aesthetic Egg Timer – React + Electron",
    "Aesthetic Weather App – API-based Frontend"
]

for project in projects:
    c.setFont("Jost-Bold", 11)
    c.drawString(margin + 10, y, project)
    y -= 16

# ---------- PROJECT IMAGE PLACEHOLDERS ----------
y -= 30
c.setFillColor(SOFT_GREEN)
c.roundRect(margin, y - 100, 220, 100, 14, fill=1, stroke=0)
c.roundRect(margin + 250, y - 100, 220, 100, 14, fill=1, stroke=0)

c.setFillColor(PRIMARY)
c.setFont("Jost", 10)
c.drawCentredString(margin + 110, y - 55, "Project Image")
c.drawCentredString(margin + 360, y - 55, "Project Image")

# ---------- SAVE ----------
c.save()
print("Portfolio PDF created with Jost font and boxed certificates.")
