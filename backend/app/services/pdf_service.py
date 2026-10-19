import io

import fitz


def extract_pages(data: bytes):

    document = fitz.open(
        stream=io.BytesIO(data),
        filetype="pdf"
    )

    pages = []

    for index, page in enumerate(document):

        text = page.get_text("text").strip()

        if text:

            pages.append({
                "page": index + 1,
                "text": text
            })

    return pages

def chunk_pages(
    pages,
    chunk_size=1200,
    overlap=200
):

    chunks = []

    for page in pages:

        text = " ".join(
            page["text"].split()
        )

        start = 0

        while start < len(text):

            end = min(
                start + chunk_size,
                len(text)
            )

            chunk = text[start:end].strip()

            if chunk:

                chunks.append({
                    "page": page["page"],
                    "text": chunk
                })

            if end >= len(text):
                break

            start = max(
                0,
                end - overlap
            )

    return chunks