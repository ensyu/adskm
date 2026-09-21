"""Audit Log Schema (Pydantic v2)."""
from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict


AuditAction = Literal[
    "create",
    "update",
    "approve",
    "reject",
    "review",
    "escalate",
    "supersede",
]


class AuditEntry(BaseModel):
    """Single audit log entry (immutable record)."""

    model_config = ConfigDict(validate_assignment=True)

    timestamp: str = Field(...)  # ISO 8601 datetime
    change_id: str = Field(...)  # Unique identifier
    who: str = Field(..., max_length=128)
    action: AuditAction
    knowledge_id: str = Field(
        ...,
        pattern=r"^KNW-[A-Z0-9]{3}-[A-Z0-9]{3}-[0-9]{3}$",
    )
    previous_version: Optional[str] = Field(None, pattern=r"^\d+\.\d+\.\d+$")
    new_version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    previous_status: Optional[str] = None
    new_status: str
    evidence_changed: bool = False
    field_changed: list[str] = Field(default_factory=list)
    reason: Optional[str] = Field(None, max_length=1000)
    approval_comment: Optional[str] = Field(None, max_length=2000)
    security_notes: Optional[str] = Field(None, max_length=1000)


def create_audit_entry(
    change_id: str,
    who: str,
    action: AuditAction,
    knowledge_id: str,
    new_version: str,
    new_status: str,
    timestamp: str,
    **kwargs,
) -> AuditEntry:
    """Factory function to create audit entry."""
    return AuditEntry(
        timestamp=timestamp,
        change_id=change_id,
        who=who,
        action=action,
        knowledge_id=knowledge_id,
        new_version=new_version,
        new_status=new_status,
        **kwargs,
    )
