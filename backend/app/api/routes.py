import uuid

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile
)
from app.core.config import settings
from app.services.ollama_service import generate
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.database import get_db
from app.models.document import Document

from app.services.s3_service import upload_bytes

from app.services.pdf_service import (
    extract_pages,
    chunk_pages
)

from app.services.ollama_service import embed

from app.services import qdrant_service


router = APIRouter()


@router.post("/documents/upload")
async def upload_document(

    file: UploadFile = File(...),

    db: Session = Depends(get_db)
):

    if file.content_type != "application/pdf":

        raise HTTPException(
            400,
            "Only PDF files are supported"
        )

    data = await file.read()

    if len(data) > 5 * 1024 * 1024:

        raise HTTPException(
            400,
            "Maximum file size is 5 MB"
        )

    document_id = str(
        uuid.uuid4()
    )

    s3_key = (
        f"documents/"
        f"{document_id}/"
        f"{file.filename}"
    )

    document = Document(

        id=document_id,

        filename=file.filename,

        s3_key=s3_key,

        status="processing"
    )

    db.add(document)
    db.commit()

    try:

        # 1. Store original PDF
        upload_bytes(
            s3_key,
            data,
            file.content_type
        )

        # 2. Extract text
        pages = extract_pages(data)

        # 3. Create chunks
        chunks = chunk_pages(pages)

        if not chunks:

            raise ValueError(
                "No extractable text found in PDF"
            )

        # 4. Create embeddings
        vectors = []

        for chunk in chunks:

            vector = await embed(
                chunk["text"]
            )

            vectors.append(vector)

        # 5. Create Qdrant collection
        qdrant_service.ensure_collection(
            len(vectors[0])
        )

        # 6. Store vectors
        qdrant_service.upsert_chunks(

            document_id,

            chunks,

            vectors
        )

        document.status = "ready"

        document.chunk_count = len(chunks)

        db.commit()

        return {

            "id": document_id,

            "filename": file.filename,

            "status": "ready",

            "chunks": len(chunks)
        }

    except Exception as exc:

        document.status = "failed"

        document.error_message = str(exc)

        db.commit()

        raise HTTPException(
            500,
            f"Ingestion failed: {exc}"
        )
    
@router.post("/chat")
async def chat(payload: dict):

    question = str(
        payload.get("question", "")
    ).strip()

    if not question:

        raise HTTPException(
            400,
            "question is required"
        )

    # 1. Question → embedding

    question_vector = await embed(
        question
    )

    # 2. Search Qdrant

    hits = qdrant_service.search(

        question_vector,

        settings.top_k
    )

    contexts = []

    sources = []

    for hit in hits:

        payload = hit.payload or {}

        contexts.append(

            f"[Page {payload.get('page')}] "
            f"{payload.get('text', '')}"
        )

        sources.append({

            "document_id":
                payload.get("document_id"),

            "page":
                payload.get("page"),

            "score":
                hit.score
        })

    # 3. Combine retrieved chunks

    context = "\n\n".join(
        contexts
    )

    # 4. Grounded prompt

    prompt = f"""
You are a document question-answering assistant.

Answer using only the provided context.

If the context does not contain the answer, say:

"I could not find that information in the uploaded documents."

Be concise and mention page numbers when useful.

CONTEXT:

{context}

QUESTION:

{question}

ANSWER:
"""

    # 5. Send context + question to LLM

    answer = await generate(
        prompt
    )

    return {

        "answer": answer,

        "sources": sources
    }