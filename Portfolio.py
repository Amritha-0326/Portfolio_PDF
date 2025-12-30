from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)
from reportlab.platypus import Flowable
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------- PATHS ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE_DIR, "fonts")
IMG_DIR = os.path.join(BASE_DIR, "images")

# ---------- FONTS ----------
pdfmetrics.registerFont(
    TTFont("Jost", os.path.join(FONT_DIR, "Jost-Regular.ttf")))
pdfmetrics.registerFont(
    TTFont("Jost-Bold", os.path.join(FONT_DIR, "Jost-Bold.ttf")))

# ---------- COLORS ----------
PRIMARY = HexColor("#4C5C68")
ACCENT = HexColor("#B6A58D")
CTA = HexColor("#C37052")
SOFT_GREEN = HexColor("#B8CA93")
CARD_BG = HexColor("#F7F6F4")
WHITE = HexColor("#FFFFFF")
BLACK = HexColor("#000000")
TAG_BG = HexColor("#DDDDDD")
WHITE_BG = HexColor("#F3F2ED")

# ---------- DOCUMENT ----------
doc = SimpleDocTemplate(
    "Amritha_Portfolio.pdf",
    pagesize=A4,
    rightMargin=50,
    leftMargin=50,
    # topMargin=280,
    bottomMargin=50
)

story = []

# ---------FUNCTIONS---------


def draw_header(canvas, doc):
    width, height = A4
    header_height = 50

    # White background box
    canvas.setFillColor(WHITE)
    canvas.rect(0, height - header_height, width,
                header_height, fill=1, stroke=0)

    # Left text: Name
    canvas.setFont("Jost-Bold", 16)
    canvas.setFillColor(PRIMARY)
    # 36 = vertical padding
    canvas.drawString(50, height - 36, "Amritha P Anil")

    # Right button: Contact Me
    btn_width = 100
    btn_height = 30
    btn_x = width - 50 - btn_width
    btn_y = height - 40  # small padding from top

    # Draw rounded rectangle
    radius = 5
    canvas.setFillColor(CTA)
    canvas.roundRect(btn_x, btn_y, btn_width, btn_height,
                     radius, fill=1, stroke=0)

    # Button text
    canvas.setFont("Jost-Bold", 12)
    canvas.setFillColor(WHITE)
    text_width = canvas.stringWidth("Contact Me", "Jost-Bold", 12)
    text_x = btn_x + (btn_width - text_width) / 2
    text_y = btn_y + (btn_height - 12) / 2 + 3  # approx vertical centering
    canvas.drawString(text_x, text_y, "Contact Me")


def draw_round_image(canvas, image_path, x, y, size, border_width=4):
    canvas.saveState()

    # Draw white border (slightly bigger circle)
    canvas.setFillColorRGB(1, 1, 1)  # white
    canvas.circle(
        x + size / 2,
        y + size / 2,
        size / 2 + border_width,
        stroke=0,
        fill=1
    )

    # Clip for circular image
    path = canvas.beginPath()
    path.circle(
        x + size / 2,
        y + size / 2,
        size / 2
    )
    canvas.clipPath(path, stroke=0, fill=0)

    # Draw the image inside the circle
    canvas.drawImage(
        ImageReader(image_path),
        x,
        y,
        width=size,
        height=size,
        mask="auto"
    )

    canvas.restoreState()


def draw_banner(canvas, doc):
    width, height = A4
    # Green header background (taller)
    canvas.setFillColor(SOFT_GREEN)
    canvas.rect(0, height - 260, width, 260, fill=1, stroke=0)

    # Profile image (round)
    draw_round_image(
        canvas,
        os.path.join(IMG_DIR, "profile.jpg"),
        x=60,
        y=height - 200,
        size=100
    )

    # Name
    canvas.setFillColor(PRIMARY)
    canvas.setFont("Jost-Bold", 24)
    canvas.drawString(190, height - 120, "Amritha Preetha Anil")

    # Subtitle (INSIDE green box)
    canvas.setFont("Jost", 13)
    canvas.drawString(
        190,
        height - 155,
        "UX Designer solving complex problems with simple interactions"
    )


def draw_skill_boxes(canvas, skills, x_start, y_start, box_height=30, padding=12, spacing=10, max_width=440):
    canvas.saveState()
    canvas.setFont("Jost-Bold", 11)
    canvas.setFillColor(PRIMARY)

    x = x_start
    y = y_start

    for skill in skills:
        # calculate width based on text
        text_width = canvas.stringWidth(skill, "Jost-Bold", 11)
        box_width = text_width + 2 * padding

        # wrap to next line if exceeds max_width
        if x + box_width > x_start + max_width:
            x = x_start
            y -= box_height + spacing

        # draw rounded rectangle
        canvas.setFillColor(ACCENT)
        canvas.roundRect(x, y - box_height, box_width,
                         box_height, radius=6, fill=1, stroke=0)

        # draw text centered
        canvas.setFillColor(PRIMARY)
        canvas.drawCentredString(x + box_width/2, y - box_height/2 - 4, skill)

        # move x for next box
        x += box_width + spacing

    canvas.restoreState()


def draw_first_page(canvas, doc):
    # draw_header(canvas, doc)
    draw_banner(canvas, doc)

    skills = ["Research", "UI Design", "Prototyping",
              "User Testing", "Prototyping Tools"]

    # Draw skills below the banner (adjust y_start as needed)
    draw_skill_boxes(
        canvas,
        skills,
        x_start=80,
        y_start=450,  # distance from bottom of page
        box_height=30,
        padding=10,
        spacing=12,
        max_width=460
    )


# ---------- STYLES ----------
frame_first = Frame(
    50, 50,
    A4[0] - 100,
    A4[1] - 330,   # space for big header
    id="first"
)

frame_later = Frame(
    50, 50,
    A4[0] - 100,
    A4[1] - 100,   # normal top margin
    id="later"
)

first_page = PageTemplate(
    id="FirstPage",
    frames=frame_first,
    onPage=draw_header
)

later_pages = PageTemplate(
    id="LaterPages",
    frames=frame_later,
    onPage=draw_header
)


title = ParagraphStyle(
    "Title",
    fontName="Jost-Bold",
    fontSize=22,
    textColor=PRIMARY,
    spaceAfter=10
)

subtitle = ParagraphStyle(
    "Subtitle",
    fontName="Jost",
    fontSize=12,
    textColor=PRIMARY,
    spaceAfter=20
)

section = ParagraphStyle(
    "Section",
    fontName="Jost-Bold",
    fontSize=15,
    textColor=PRIMARY,
    spaceBefore=20,
    spaceAfter=12,
    alignment=1
)

body = ParagraphStyle(
    "Body",
    fontName="Jost",
    fontSize=11,
    textColor=PRIMARY,
    leading=16,
    alignment=1
)
# ---------CLASSES---------

PAGE_WIDTH, _ = A4


class CertificateCards(Flowable):
    def __init__(self, certificates, width=100, box_height=60, spacing=15, left_padding=12):

        super().__init__()
        self.certificates = certificates
        self.width = width
        self.box_height = box_height
        self.spacing = spacing
        self.left_padding = left_padding
        self.height = len(certificates) * (box_height + spacing)

    def draw(self):
        c = self.canv
        y_start = 0
        x_start = ((PAGE_WIDTH - self.width) / 2) - 52  # center horizontally
        c.saveState()
        for cert in self.certificates:
            if len(cert) == 4:
                title_text, subtitle_text, color_hex, url = cert
            else:
                title_text, subtitle_text, color_hex = cert
                url = None

            bg_color = HexColor(color_hex)

            # Draw rounded rectangle (centered)
            c.setFillColor(bg_color)
            c.roundRect(x_start, y_start, self.width,
                        self.box_height, radius=8, fill=1, stroke=0)

            # Draw title and subtitle
            c.setFillColor(HexColor("#FFFFFF"))
            text_x = x_start + self.left_padding
            text_y = y_start + self.box_height - 18

            c.setFont("Jost-Bold", 12)
            c.drawString(text_x, text_y - 5, title_text)

            c.setFont("Jost", 10)
            c.drawString(text_x, text_y - 23, subtitle_text)

            # Draw "View Certificate" link
            if url:
                link_text = "View Certificate"
                link_x = text_x
                link_y = text_y - 32
                c.setFillColor(HexColor("#FFFFFF"))
                c.setFont("Jost-Bold", 9)
                c.drawString(link_x, link_y - 14, link_text)

                link_width = c.stringWidth(link_text, "Jost-Bold", 9)
                c.linkURL(url,
                          rect=(link_x, link_y - 14, link_x +
                                link_width, link_y + 10),
                          relative=1,
                          thickness=0,
                          color=None)

            # Move y_start for next card
            y_start += self.box_height + self.spacing
        c.restoreState()


class ProjectCard(Flowable):
    def __init__(
        self,
        title,
        subtitle,
        description,
        tags,
        learned,
        icon="",
        width=260,
        height=175,
        padding=14,
    ):
        super().__init__()
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.tags = tags
        self.learned = learned
        self.icon = icon
        self.width = width
        self.height = height
        self.padding = padding

    def drawAt(self, x, y, canvas):
        self.canv = canvas
        self._x = x - 55
        self._y = y
        self.draw()

    def draw(self):
        c = self.canv
        x = self._x
        y = self._y

        c.saveState()

        # Card background
        c.setFillColor(WHITE_BG)
        c.roundRect(x, y, self.width, self.height, 10, fill=1, stroke=0)

        cursor_y = y + self.height - self.padding - 5
        text_x = x + self.padding

        # Icon + title
        c.setFont("Jost-Bold", 13)
        c.setFillColor(PRIMARY)
        c.drawString(text_x, cursor_y, f"{self.icon}  {self.title}")
        cursor_y -= 18

        # Subtitle
        c.setFont("Jost", 10)
        c.drawString(text_x, cursor_y, self.subtitle)
        cursor_y -= 16

        # Description
        c.setFont("Jost", 9.5)
        text = c.beginText(text_x, cursor_y)
        text.setLeading(13)
        for line in self._wrap(self.description, c, 9.5):
            text.textLine(line)
        c.drawText(text)
        cursor_y = text.getY() - 10

        # Tags
        tag_x = text_x
        c.setFont("Jost", 8.5)
        for tag in self.tags:
            w = c.stringWidth(tag, "Jost", 8.5) + 10
            c.setFillColor(TAG_BG)
            c.roundRect(tag_x, cursor_y - 12, w, 14, 6, fill=1, stroke=0)
            c.setFillColor(BLACK)
            c.drawCentredString(tag_x + w / 2, cursor_y - 7, tag)
            tag_x += w + 5

        cursor_y -= 22

        # Learned
        c.setFont("Jost-Bold", 9.5)
        c.setFillColor(PRIMARY)
        c.drawString(text_x, cursor_y - 5, "What I learned")
        cursor_y -= 12

        c.setFont("Jost", 9.5)
        text = c.beginText(text_x, cursor_y - 5)
        text.setLeading(13)
        for line in self._wrap(self.learned, c, 9.5):
            text.textLine(line)
        c.drawText(text)

        c.restoreState()

    def _wrap(self, text, canvas, size):
        max_width = self.width - 2 * self.padding
        words, line, lines = text.split(), "", []
        for w in words:
            test = line + w + " "
            if canvas.stringWidth(test, "Jost", size) <= max_width:
                line = test
            else:
                lines.append(line)
                line = w + " "
        if line:
            lines.append(line)
        return lines


class ProjectGrid(Flowable):
    def __init__(self, cards, spacing=20):
        super().__init__()
        self.cards = cards
        self.spacing = spacing
        self.cols = 2

        self.card_width = cards[0].width
        self.card_height = cards[0].height

        rows = (len(cards) + 1) // 2
        self.width = PAGE_WIDTH
        self.height = rows * (self.card_height + spacing)

    def draw(self):
        c = self.canv
        x_start = (PAGE_WIDTH - (2 * self.card_width + self.spacing)) / 2
        y = self.height - self.card_height

        for i, card in enumerate(self.cards):
            col = i % 2
            if col == 0 and i != 0:
                y -= self.card_height + self.spacing

            x = x_start + col * (self.card_width + self.spacing)
            card.drawAt(x, y, c)


class ImageCard(Flowable):
    def __init__(self, image_path, width=200, height=240, radius=12, border=4):
        super().__init__()
        self.image_path = image_path
        self.width = width
        self.height = height
        self.radius = radius
        self.border = border

    def drawAt(self, x, y, canvas):
        self.canv = canvas
        self._x = x
        self._y = y
        self.draw()

    def draw(self):
        c = self.canv
        x = self._x
        y = self._y

        c.saveState()

        # White rounded border
        c.setFillColor(WHITE_BG)
        c.roundRect(
            x - self.border,
            y - self.border,
            self.width + self.border * 2,
            self.height + self.border * 2,
            self.radius + self.border,
            fill=1,
            stroke=0
        )

        # Clip rounded image
        path = c.beginPath()
        path.roundRect(x, y, self.width, self.height, self.radius)
        c.clipPath(path, stroke=0, fill=0)

        c.drawImage(
            ImageReader(self.image_path),
            x,
            y,
            width=self.width,
            height=self.height,
            mask="auto"
        )

        c.restoreState()


class ProjectImageGrid(Flowable):
    def __init__(self, images, spacing=30):
        super().__init__()
        self.images = images
        self.spacing = spacing
        self.cols = 2

        self.card_width = images[0].width
        self.card_height = images[0].height

    def wrap(self, availWidth, availHeight):
        rows = (len(self.images) + 1) // 2
        self.width = availWidth
        self.height = rows * (self.card_height + self.spacing)
        return self.width, self.height

    def split(self, availWidth, availHeight):
        rows_that_fit = int(
            availHeight // (self.card_height + self.spacing)
        )

        if rows_that_fit <= 0:
            return []

        max_images = rows_that_fit * 2
        first = self.images[:max_images]
        rest = self.images[max_images:]

        flowables = [ProjectImageGrid(first, self.spacing)]
        if rest:
            flowables.append(ProjectImageGrid(rest, self.spacing))

        return flowables

    def draw(self):
        c = self.canv

        total_row_width = self.card_width * 2 + self.spacing
        x_start = (self.width - total_row_width) / 2
        y = self.height - self.card_height

        for i, card in enumerate(self.images):
            col = i % 2
            if col == 0 and i != 0:
                y -= self.card_height + self.spacing

            x = x_start + col * (self.card_width + self.spacing)
            card.drawAt(x, y, c)


# ---------- OVERVIEW ----------
story.append(Spacer(1, 185))
story.append(Paragraph("Professional Overview", section))
story.append(
    Paragraph(
        "I’m just starting out as a UX designer, but I’m already passionate about turning "
        "user needs into intuitive, meaningful experiences. I bring curiosity, attention "
        "to detail, and a research-driven mindset to every project.",
        body
    )
)
story.append(Spacer(1, 80))

# ---------- CERTIFICATES DATA ----------
certificates = [
    ("UX Research & Early Testing", "Google Career Certificate · 2025",
     "#4c5c68", "https://coursera.org/verify/NM7EE4NTFUQG"),
    ("UX Design Process", "Google Career Certificate · 2023", "#b87b5a",
     "https://coursera.org/verify/HVDVFMEQLPZK"),
    ("Foundations of UX Design", "Google Career Certificate · 2021",
     "#8b9a7a", "https://coursera.org/verify/8G87LVSUC5CC")
]
certificates1 = [
    ("React Basics", "Meta · In Progress", "#8b9a7a"),
    ("Unit Testing in React.js", "Coursera · 2025", "#cbbfb0",
     "https://coursera.org/share/489f522143b954e11686213c8728e81f")
]

story.append(Paragraph(
    "Certificates & Achievements",
    ParagraphStyle(
        "Section", fontName="Jost-Bold", fontSize=15, textColor=HexColor("#4C5C68"),
        spaceBefore=20, spaceAfter=12, alignment=1
    )
))

story.append(CertificateCards(
    certificates, width=200, box_height=80, spacing=15))
story.append(Spacer(0, 10))
story.append(CertificateCards(
    certificates1, width=200, box_height=80, spacing=15))
story.append(Spacer(0, 10))

# ---------- PROJECTS ----------
story.append(Paragraph("Fun Projects & Learning", section))
story.append(Spacer(1, 10))

projects = [
    ProjectCard(
        title="Aesthetic Egg Timer",
        subtitle="Desktop UI Experiment · React + Electron",
        description=(
            "A retro pixel-art style egg timer with three preset options. "
            "Built using React and packaged with Electron."
        ),
        tags=["React", "Electron", "UI Design", "Pixel Art"],
        learned=(
            "Learned how to combine React logic with Electron and design "
            "simple but delightful timer-based interactions."
        ),
        icon="🥚"
    ),
    ProjectCard(
        title="Aesthetic Weather App",
        subtitle="API-Based Frontend Project",
        description=(
            "An aesthetic weather app inspired by the Egg Timer visual style. "
            "Uses OpenWeatherMap API with city search and error handling."
        ),
        tags=["API Integration", "Frontend", "UI Design", "Async States"],
        learned=(
            "Working with real-time data requires careful handling of loading "
            "and error states while maintaining visual consistency."
        ),
        icon="☁️"
    )
]

story.append(ProjectGrid(projects))

image_cards = [
    ImageCard(os.path.join(IMG_DIR, "project1.jpg")),
    ImageCard(os.path.join(IMG_DIR, "project2.jpg")),
]

story.append(ProjectImageGrid(image_cards))
story.append(Spacer(1, 30))


# ---------- BUILD ----------
doc.build(
    story,
    onFirstPage=draw_first_page,  # header + banner
    onLaterPages=draw_header       # only compact header
)


print("Multi-page portfolio PDF created successfully.")
