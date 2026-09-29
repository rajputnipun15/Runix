"""TerminalSession model — tracks interactive terminal connections."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TerminalSession(Base):
    __tablename__ = "terminal_sessions"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'closed', 'failed')",
            name="terminal_session_status_check",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    runtime_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("runtimes.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="active")
    shell: Mapped[str] = mapped_column(String(100), nullable=False, default="/bin/bash")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    runtime = relationship("Runtime", back_populates="terminal_sessions")
    user = relationship("User")
