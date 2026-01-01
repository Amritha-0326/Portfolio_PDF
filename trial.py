# from pypdf import PdfReader
# import os
# print("Running from:", os.getcwd())

# reader = PdfReader("Amritha_Portfolio.pdf")

# for i, page in enumerate(reader.pages):
#     w = float(page.mediabox.width)
#     h = float(page.mediabox.height)
#     print(f"Page {i+1}: {w:.0f} × {h:.0f} points")

from pypdf import PdfReader, PdfWriter
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PDF = os.path.join(BASE_DIR, "Homepage_case_study.pdf")
OUTPUT_PDF = os.path.join(BASE_DIR, "Homepage_case_study_A4width.pdf")

A4_WIDTH = 595
A4_HEIGHT = 842

reader = PdfReader(INPUT_PDF)
writer = PdfWriter()

for page in reader.pages:
    orig_w = float(page.mediabox.width)
    orig_h = float(page.mediabox.height)

    scale = A4_WIDTH / orig_w
    new_h = orig_h * scale

    new_page = writer.add_blank_page(
        width=A4_WIDTH,
        height=new_h
    )

    new_page.merge_scaled_page(page, scale, scale)

with open(OUTPUT_PDF, "wb") as f:
    writer.write(f)
