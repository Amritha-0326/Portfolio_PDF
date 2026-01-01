from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.platypus import Flowable
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak

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
    bottomMargin=50
)

story = []

# ---------FUNCTIONS---------


def draw_header(canvas, doc):
    width, height = A4
    header_height = 50

    # White background box
    canvas.setFillColor(WHITE_BG)
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
    # radius = 5
    # canvas.setFillColor(CTA)
    # canvas.roundRect(btn_x, btn_y, btn_width, btn_height,
    #                  radius, fill=1, stroke=0)

    # Button text
    canvas.setFont("Jost-Bold", 16)
    canvas.setFillColor(WHITE)
    text_width = canvas.stringWidth(
        "“Design. Iterate. Repeat.”", "Jost-Bold", 12)
    text_x = btn_x + (btn_width - text_width) / 2
    text_y = btn_y + (btn_height - 12) / 2 + 3  # approx vertical centering
    canvas.drawString(text_x, text_y, "“Design. Iterate. Repeat.”")


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
        x_start=70,
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

PAGE_WIDTH, PAGE_HEIGHT = A4


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
        width=270,
        height=245,
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
        self._x = x
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
        cursor_y = cursor_y - 5
        c.setFont("Jost-Bold", 9.5)
        c.setFillColor(PRIMARY)
        c.drawString(text_x, cursor_y - 5, "What I learned")
        cursor_y -= 12

        c.setFont("Jost", 9.5)
        text = c.beginText(text_x, cursor_y - 8)
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


class CopyrightCard(Flowable):
    def __init__(
        self,
        text="© 2025 Amritha Preetha Anil. All rights reserved.",
        height=15,
    ):
        super().__init__()
        self.text = text
        self.height = height

    def wrap(self, availWidth, availHeight):
        # Take full available width, fixed height
        self.width = availWidth + 80
        return self.width, self.height

    def draw(self):
        c = self.canv

        # Background bar
        c.setFillColor(SOFT_GREEN)
        c.rect(
            -80,
            -60,
            (self.width) + 150,
            self.height,
            fill=1,
            stroke=0
        )

        # Text (centered)
        c.setFont("Jost", 9)
        c.setFillColor(WHITE)

        text_width = c.stringWidth(self.text, "Jost", 9)
        text_x = ((self.width - text_width) / 2) - 30
        text_y = ((self.height - 9) / 2 + 1) - 60  # optical vertical centering

        c.drawString(text_x, text_y, self.text)


class ImageCard(Flowable):
    def __init__(
        self,
        image_path,
        caption,
        link=None,
        width=200,
        height=250,
        radius=12,
        border=6,
    ):
        super().__init__()
        self.image_path = image_path
        self.caption = caption
        self.link = link
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
        x, y = self._x, self._y

        c.saveState()

        # White border
        c.setFillColor(WHITE)
        c.roundRect(
            x - self.border,
            y - self.border,
            self.width + self.border * 2,
            self.height + self.border * 2,
            self.radius + self.border,
            fill=1,
            stroke=0
        )

        # Clip image
        path = c.beginPath()
        path.roundRect(x, y, self.width, self.height, self.radius)
        c.clipPath(path, stroke=0, fill=0)

        c.drawImage(
            ImageReader(self.image_path),
            x, y,
            width=self.width,
            height=self.height,
            mask="auto"
        )

        # Caption overlay
        caption_height = 28
        c.setFillColor(WHITE_BG)
        c.rect(x, y, self.width, caption_height, fill=1, stroke=0)

        c.setFont("Jost-Bold", 9)
        c.setFillColor(HexColor("#8b9a7a"))
        c.drawCentredString(
            x + self.width / 2,
            y + 9,
            self.caption
        )

        # Clickable area
        if self.link:
            c.linkURL(
                self.link,
                (x, y, x + self.width, y + self.height),
                relative=1
            )

        c.restoreState()


class TwoColumnGrid(Flowable):
    def __init__(self, items, spacing=30):
        super().__init__()
        self.items = items
        self.spacing = spacing
        self.cols = 2

        self.item_width = items[0].width
        self.item_height = items[0].height

    def wrap(self, availWidth, availHeight):
        rows = (len(self.items) + 1) // 2
        self.width = availWidth
        self.height = rows * (self.item_height + self.spacing)
        return self.width, self.height

    def split(self, availWidth, availHeight):
        rows_fit = int(availHeight // (self.item_height + self.spacing))
        if rows_fit <= 0:
            return []

        max_items = rows_fit * 2
        return [
            TwoColumnGrid(self.items[:max_items], self.spacing),
            TwoColumnGrid(self.items[max_items:], self.spacing)
        ] if len(self.items) > max_items else []

    def draw(self):
        c = self.canv
        total_width = self.item_width * 2 + self.spacing
        x_start = (self.width - total_width) / 2
        y = self.height - self.item_height

        for i, item in enumerate(self.items):
            col = i % 2
            if col == 0 and i != 0:
                y -= self.item_height + self.spacing

            x = x_start + col * (self.item_width + self.spacing)
            item.drawAt(x, y, c)


class LetsConnectCard(Flowable):
    def __init__(
        self,
        email="amrithapanil0326@gmail.com",
        location="Germany",
        links=None,
        card_width=380,
        card_height=220,
    ):
        super().__init__()

        self.email = email
        self.location = location
        self.card_width = card_width
        self.card_height = card_height

        self.links = links or [
            ("LinkedIn", "https://www.linkedin.com/in/amritha-p-8anil89700/"),
            ("Behance", "https://www.behance.net/amrithaanil"),
            ("GitHub", "https://github.com/Amritha-0326"),
        ]

        # This Flowable only occupies vertical space equal to its content
        self.width = A4[0]
        self.height = card_height + 160

    def wrap(self, availWidth, availHeight):
        return availWidth, self.height

    def _draw_social_boxes(self, c, center_x, y):
        c.saveState()

        c.setFont("Jost-Bold", 11)
        c.setFillColor(PRIMARY)

        padding_x = 14
        box_height = 34
        spacing = 55

        # Calculate total width first (to center group)
        box_data = []
        total_width = 0

        for label, url in self.links:
            text_width = c.stringWidth(label, "Jost-Bold", 11)
            box_width = text_width + padding_x * 2
            box_data.append((label, url, box_width))
            total_width += box_width

        total_width += spacing * (len(box_data) - 1)

        # Starting x so entire group is centered
        x = (center_x - total_width / 2)

        for label, url, box_width in box_data:
            # Draw rounded rectangle
            c.setFillColor(HexColor("#abc686"))
            c.roundRect(
                x,
                (y - box_height) + 10,
                box_width,
                box_height,
                radius=8,
                fill=1,
                stroke=0
            )

            # Draw label
            c.setFillColor(WHITE)
            text_y = y - box_height / 2 - 4
            c.drawCentredString(x + box_width / 2, text_y + 10, label)

            # Clickable area
            c.linkURL(
                url,
                (
                    x,
                    y - box_height,
                    x + box_width,
                    y,
                ),
                relative=1
            )

            x += box_width + spacing

        c.restoreState()

    def draw(self):
        c = self.canv
        width, _ = A4

        # ---------- Centering ----------
        center_x = (width / 2) - 60
        y_base = self.height - 40

        # ---------- Title ----------
        c.setFont("Jost-Bold", 26)
        c.setFillColor(PRIMARY)
        c.drawCentredString(center_x, y_base, "Let’s Connect")

        # ---------- Card ----------
        card_x = center_x - self.card_width / 2
        card_y = y_base - self.card_height - 30

        c.setFillColor(PRIMARY)
        c.roundRect(
            card_x,
            card_y,
            self.card_width,
            self.card_height,
            18,
            fill=1,
            stroke=0
        )

        # ---------- Card Content ----------
        text_x = card_x + 40
        text_y = card_y + self.card_height - 55

        c.setFillColor(WHITE)
        c.setFont("Jost-Bold", 16)
        c.drawString(text_x, text_y, "Contact Info")

        c.setFont("Jost", 12)
        c.drawString(text_x, text_y - 40, "Email")
        c.setFont("Jost-Bold", 12)
        c.drawString(text_x, text_y - 60, self.email)

        c.setFont("Jost", 12)
        c.drawString(text_x, text_y - 95, "Based in")
        c.setFont("Jost-Bold", 12)
        c.drawString(text_x, text_y - 115, self.location)

        # ---------- Social Links Container ----------
        container_width = 420
        container_height = 46
        container_x = center_x - container_width / 2
        container_y = card_y - 60

        self._draw_social_boxes(c, center_x, container_y)


class PersonalPassion(Flowable):
    def __init__(
        self,
        width=A4[0] - 100,
        card_width=160,
        card_height=260,
        spacing=30,
    ):
        super().__init__()
        self.width = width
        self.card_width = card_width
        self.card_height = card_height + 50
        self.spacing = spacing

        self.height = card_height + 160  # total vertical space

        self.cards = [
            {
                "title": "Weekend Sketches",
                "text": (
                    "Sketching helps me see. It sharpens my eye for detail and keeps "
                    "my creative instincts grounded, just like good design should."
                ),
                "image": os.path.join(IMG_DIR, "passion-image.jpg"),
            },
            {
                "title": "Scent & Sensibility",
                "text": (
                    "I’m drawn to the layers, balance, and emotion behind a well-crafted "
                    "fragrance. It is storytelling through subtle detail."
                ),
                "image": os.path.join(IMG_DIR, "scent.png"),
            },
            {
                "title": "Matcha Rituals",
                "text": (
                    "The quiet ritual of making matcha reminds me to slow down, "
                    "stay present, and design with intention."
                ),
                "image": os.path.join(IMG_DIR, "matcha.png"),
            },
        ]

    def wrap(self, availWidth, availHeight):
        return availWidth, self.height

    def _draw_cover_image(self, c, image_path, x, y, box_w, box_h):
        img = ImageReader(image_path)
        img_w, img_h = img.getSize()

        img_ratio = img_w / img_h
        box_ratio = box_w / box_h

        if img_ratio > box_ratio:
            # image is wider → crop sides
            draw_h = box_h
            draw_w = box_h * img_ratio
        else:
            # image is taller → crop top/bottom
            draw_w = box_w
            draw_h = box_w / img_ratio

        draw_x = x - (draw_w - box_w) / 2
        draw_y = y - (draw_h - box_h) / 2

        c.drawImage(
            img,
            draw_x,
            draw_y,
            width=draw_w,
            height=draw_h,
            mask="auto"
        )

    def draw(self):
        c = self.canv
        page_width, _ = A4

        center_x = (page_width / 2) - 75
        start_y = self.height - 40

        # ---------- Section Title ----------
        c.setFont("Jost-Bold", 18)
        c.setFillColor(PRIMARY)
        c.drawCentredString(center_x + 15, start_y, "Personal Passion")

        # ---------- Cards Layout ----------
        total_width = (self.card_width * 3) + (self.spacing * 2)
        x_start = center_x - (total_width / 2)
        y_card = start_y - self.card_height - 40

        for i, card in enumerate(self.cards):
            x = (x_start + i * (self.card_width + self.spacing)) + 20

            self._draw_card(
                c,
                x,
                y_card,
                card["image"],
                card["title"],
                card["text"],
            )

        # ---------- Footer Text ----------
        footer_text = (
            "My work is shaped by more than just tools and techniques – it’s shaped by "
            "the things I care about. Whether it’s sketching on the weekends or getting "
            "lost in the quiet details of everyday life, the more grounded I am outside "
            "the screen, the more empathy and clarity I bring into my designs."
        )
        x_gap = 10
        text = c.beginText(x_gap, y_card - 60)
        text.setFont("Jost", 11)
        text.setFillColor(PRIMARY)
        text.setLeading(16)

        max_width = page_width - 120
        words, line = footer_text.split(), ""

        for word in words:
            test = line + word + " "
            if c.stringWidth(test, "Jost", 11) <= max_width:
                line = test
            else:
                text.textLine(line)
                line = word + " "
        if line:
            text.textLine(line)

        c.drawText(text)

    def _draw_card(self, c, x, y, image_path, title, text):
        c.saveState()

        # ---------- Card Background ----------
        c.setFillColor(CARD_BG)
        c.roundRect(
            x,
            y,
            self.card_width,
            self.card_height,
            14,
            fill=1,
            stroke=0
        )

        # ---------- Image (CLIPPED) ----------
        img_height = 170
        c.saveState()  # 🔑 isolate clipping

        path = c.beginPath()
        path.roundRect(
            x,
            y + self.card_height - img_height,
            self.card_width,
            img_height,
            14
        )
        c.clipPath(path, stroke=0, fill=0)

        self._draw_cover_image(
            c,
            image_path,
            x,
            y + self.card_height - img_height,
            self.card_width,
            img_height
        )
        c.restoreState()  # 🔑 clipping ends here

        # ---------- Text ----------
        text_x = x + 14
        cursor_y = y + self.card_height - img_height - 26

        c.setFillColor(PRIMARY)
        c.setFont("Jost-Bold", 12)
        c.drawCentredString(
            x + self.card_width / 2,
            cursor_y,
            title
        )

        cursor_y -= 18
        c.setFont("Jost", 9.8)

        text_obj = c.beginText(text_x, cursor_y)
        text_obj.setLeading(14)

        max_width = self.card_width - 28
        words, line = text.split(), ""

        for word in words:
            test = line + word + " "
            if c.stringWidth(test, "Jost", 9.8) <= max_width:
                line = test
            else:
                text_obj.textLine(line)
                line = word + " "
        if line:
            text_obj.textLine(line)

        c.drawText(text_obj)
        c.restoreState()


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
story.append(Spacer(0, 10))

story.append(CertificateCards(
    certificates, width=200, box_height=80, spacing=15))
story.append(Spacer(0, 10))
story.append(CertificateCards(
    certificates1, width=200, box_height=80, spacing=15))
story.append(Spacer(0, 10))
story.append(PersonalPassion())

# ---------- PROJECTS ----------
story.append(Spacer(1, 10))
story.append(Paragraph("Fun Projects & Learning", section))
story.append(Spacer(1, 30))

project_cards = [
    ProjectCard(
        title="Aesthetic Egg Timer",
        subtitle="Desktop UI Experiment · React + Electron",
        description="A retro pixel-art style egg timer with three preset options, soft, runny, and hard. Built with React for the timer logic and UI, then packaged using Electron to run as a lightweight desktop application with a playful, nostalgic aesthetic.",
        tags=["React", "Electron", "UI Design", "Desktop App", "Pixel Art"],
        learned="How to combine React logic with Electron to create a desktop app, structure timer-based state effectively, and design a clear, fun interface without overcomplicating functionality.",
        icon="🥚"
    ),
    ProjectCard(
        title="Aesthetic Weather App",
        subtitle="API-Based Frontend Project",
        description="Created an aesthetic weather application inspired by the Egg Timer’s visual style. The app fetches real-time weather data from the OpenWeatherMap API and supports city-based search, a custom color palette, and clear loading and error states.",
        tags=["API Integration", "Frontend", "UI Design", "Async States"],
        learned="Working with real-time data requires thoughtful handling of loading and error states. Consistent visual design helps make technical features feel friendly and approachable.",
        icon="☁️"
    )
]

story.append(TwoColumnGrid(project_cards))
story.append(Spacer(1, 40))

image_cards = [
    ImageCard(
        os.path.join(IMG_DIR, "project1.jpg"),
        caption="Aesthetic Egg Timer",
        link="https://github.com/Amritha-0326/Aesthetic-Egg-Timer"
    ),
    ImageCard(
        os.path.join(IMG_DIR, "project2.jpg"),
        caption="Aesthetic Weather App",
        link="https://github.com/Amritha-0326/Aesthetic-Weather-App"
    ),
]

story.append(TwoColumnGrid(image_cards))
# story.append(Spacer(1, 20))
# story.append(PersonalPassion())
story.append(Spacer(1, 60))
story.append(PageBreak())
story.append(LetsConnectCard())
story.append(Spacer(-10, 300))  # optional breathing space
story.append(CopyrightCard())


# ---------- BUILD ----------
doc.build(
    story,
    onFirstPage=draw_first_page,  # header + banner
    onLaterPages=draw_header       # only compact header
)

print("Multi-page portfolio PDF created successfully.")
