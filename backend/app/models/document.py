from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.database import Base


class Document(Base):

    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True
    )

    filename: Mapped[str] = mapped_column(
        String(255)
    )

    s3_key: Mapped[str] = mapped_column(
        String(500),
        unique=True
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="uploaded"
    )

    chunk_count: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )