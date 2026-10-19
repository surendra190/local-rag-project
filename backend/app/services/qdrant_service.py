import uuid

from qdrant_client import QdrantClient

from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)

from app.core.config import settings


client = QdrantClient(
    url=settings.qdrant_url
)


def ensure_collection(vector_size: int):

    if not client.collection_exists(
        settings.qdrant_collection
    ):

        client.create_collection(
            collection_name=settings.qdrant_collection,

            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )


def upsert_chunks(
    document_id,
    chunks,
    vectors
):

    points = []

    for index, (chunk, vector) in enumerate(
        zip(chunks, vectors)
    ):

        # Create a valid deterministic UUID for each chunk
        point_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                f"{document_id}-{index}"
            )
        )

        points.append(
            PointStruct(
                id=point_id,

                vector=vector,

                payload={
                    "document_id": str(document_id),
                    "chunk_index": index,
                    "page": chunk["page"],
                    "text": chunk["text"]
                }
            )
        )

    client.upsert(
        collection_name=settings.qdrant_collection,
        points=points
    )


def search(
    vector,
    limit
):

    result = client.query_points(
        collection_name=settings.qdrant_collection,
        query=vector,
        limit=limit,
        with_payload=True
    )

    return result.points