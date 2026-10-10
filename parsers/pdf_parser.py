from pypdf import PdfReader


def parse_pdf(pdf_doc) -> str:
    doc = PdfReader(pdf_doc)
    text = ""
    for page in doc.pages:
        text += str(page.extract_text())
    return text
