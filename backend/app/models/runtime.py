"""Runtime model — isolated execution environment metadata."""

import uuid
from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Runtime(Base):
    __tablename__ = "runtimes"
    __table_args__ = (
        CheckConstraint(
            "status IN ('creating', 'starting', 'running', 'stopping', "
            "'stopped', 'failed', 'terminating', 'terminated')",
            name="runtime_status_check",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    container_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    runtime_type: Mapped[str] = mapped_column(String(50), nullable=False)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="creating", index=True)
    cpu_limit: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), nullable=False, default=Decimal("1.00")
    )
    memory_limit_mb: Mapped[int] = mapped_column(Integer, nullable=False, default=1024)
    storage_limit_mb: Mapped[int] = mapped_column(Integer, nullable=False, default=2048)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    stopped_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    terminated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_health_check_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    project = relationship("Project", back_populates="runtimes")
    terminal_sessions = relationship(
        "TerminalSession", back_populates="runtime", cascade="all, delete-orphan"
    )
    command_executions = relationship(
        "CommandExecution", back_populates="runtime", cascade="all, delete-orphan"
    )
