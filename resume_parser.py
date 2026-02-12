import fitz
import pytesseract
from PIL import Image
import io


def extract_text_from_pdf(file):
    file.seek(0)
    file_bytes = file.read()
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""

    for page in doc:
        page_text = page.get_text().strip()

        if len(page_text) < 50:
            try:
                pix = page.get_pixmap(dpi=300)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                ocr_text = pytesseract.image_to_string(img)
                text += ocr_text + "\n"
            except Exception:
                pass
        else:
            text += page_text + "\n"

    return text


def extract_text_from_txt(file):
    return file.read().decode("utf-8")


def extract_text(file):
    if file.name.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif file.name.endswith(".txt"):
        return extract_text_from_txt(file)
    else:
        return ""
