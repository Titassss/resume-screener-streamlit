import fitz
import pytesseract
from PIL import Image
import io

def get_pdf_text(file_obj):
    file_obj.seek(0)
    data = file_obj.read()
    doc = fitz.open(stream=data, filetype="pdf")
    full_text = ""

    for page in doc:
        text = page.get_text().strip()

        if len(text) < 50:
            try:
                pix = page.get_pixmap()
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                ocr_res = pytesseract.image_to_string(img)
                full_text += ocr_res + "\n"
            except:
                pass
        else:
            full_text += text + "\n"

    return full_text


def get_file_content(file):
    if file.name.endswith(".pdf"):
        return get_pdf_text(file)
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    return ""
