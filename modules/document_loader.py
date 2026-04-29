import PyPDF2


def load_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text:
            pages.append({
                "page": page_number,
                "text": text
            })

    return pages


def pages_to_full_text(pages):
    return "\n\n".join([f"[Page {p['page']}]\n{p['text']}" for p in pages])