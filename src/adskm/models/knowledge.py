"""Knowledge Record Schema (Pydantic v2)."""
from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator


SourceType = Literal[
    "law",
    "regulation",
    "manufacturer",
    "design_document",
    "company_standard",
    "approved_procedure",
    "general_practice",
    "field_record",
    "human_input",
    "ai_structured",
]

KnowledgeType = Literal[
    "procedure",
    "requirement",
    "specification",
    "standard",
    "practice",
]

KnowledgeStatus = Literal[
    "draft",
    "review_required",
    "approved",
    "rejected",
    "superseded",
]

RiskLevel = Literal["low", "medium", "high", "critical"]
EvidenceSufficiency = Literal["sufficient", "insufficient"]
ConfidenceLevel = Literal["high", "medium", "low"]
Scope = Literal["master", "project_override"]


class SourceRecord(BaseModel):
    """Single evidence source."""

    title: str = Field(..., max_length=256)
    type: SourceType
    version: str = Field(..., max_length=32)
    location: str = Field(..., max_length=2048)
    page_reference: Optional[str] = Field(None, max_length=256)
    accessed_at: str = Field(...)  # ISO 8601 date
    confidence_level: ConfidenceLevel = "high"

    @field_validator("location")
    @classmethod
    def validate_url_if_applicable(cls, v):
        """Validate URLs: http/https only, no credentials in URL."""
        if v.startswith("http://") or v.startswith("https://"):
            # Check for credentials pattern: scheme://user:pass@host
            if "://" in v and "@" in v:
                scheme_end = v.index("://") + 3
                at_pos = v.index("@")
                # If @ comes after scheme, it's likely credentials
                if at_pos > scheme_end and ":" in v[scheme_end:at_pos]:
                    raise ValueError("Credentials not allowed in URL")
        return v


class ContentModel(BaseModel):
    """Knowledge content with sanitization."""

    title: str = Field(..., max_length=100)
    summary: str = Field(..., max_length=500)
    requirements: list[str] = Field(default_factory=list)
    checks: list[str] = Field(default_factory=list)

    @field_validator("title", "summary", mode="before")
    @classmethod
    def sanitize_strings(cls, v):
        """Remove control characters, validate UTF-8, normalize whitespace."""
        if v is None:
            return None
        if not isinstance(v, str):
            raise ValueError("Field must be string")

        # Validate UTF-8
        try:
            v.encode("utf-8", errors="strict")
        except UnicodeEncodeError:
            raise ValueError("Invalid UTF-8 sequence")

        # Normalize line endings
        v = v.replace("\r\n", "\n")

        # Remove control characters (0x00-0x08, 0x0B-0x0C, 0x0E-0x1F)
        control_chars = (
            list(range(0x00, 0x09))  # 0x00-0x08
            + [0x0B, 0x0C]  # 0x0B-0x0C
            + list(range(0x0E, 0x20))  # 0x0E-0x1F
        )
        v = "".join(c for c in v if ord(c) not in control_chars)

        # Trim spaces
        v = v.strip()
        return v


class SourceModel(BaseModel):
    """Evidence/source tracking."""

    primary_source_type: SourceType
    source_classification: SourceType
    sources: list[SourceRecord] = Field(default_factory=list)
    evidence_sufficiency: EvidenceSufficiency = "sufficient"
    evidence_notes: Optional[str] = Field(None, max_length=5000)

    @field_validator("evidence_notes", mode="before")
    @classmethod
    def sanitize_notes(cls, v):
        """Sanitize evidence notes."""
        if v is None:
            return None
        if not isinstance(v, str):
            raise ValueError("evidence_notes must be string")
        v = v.encode("utf-8", errors="strict").decode("utf-8")
        v = v.replace("\r\n", "\n").strip()
        return v


class ApprovalModel(BaseModel):
    """Approval workflow tracking."""

    created_at: str = Field(...)  # ISO 8601 datetime
    created_by: str = Field(..., max_length=128)
    reviewed_at: Optional[str] = None
    reviewed_by: Optional[str] = None
    approved_at: Optional[str] = None
    approved_by: Optional[str] = None
    approval_comment: Optional[str] = Field(None, max_length=2000)
    last_updated_at: str = Field(...)
    last_updated_by: str = Field(..., max_length=128)
    update_reason: Optional[str] = Field(None, max_length=512)

    @field_validator("approval_comment", "update_reason", mode="before")
    @classmethod
    def sanitize_approval_fields(cls, v):
        """Sanitize approval comments."""
        if v is None:
            return None
        if not isinstance(v, str):
            raise ValueError("Field must be string")
        v = v.encode("utf-8", errors="strict").decode("utf-8")
        v = v.replace("\r\n", "\n").strip()
        return v


class MetadataModel(BaseModel):
    """Knowledge metadata."""

    id: str = Field(
        ...,
        pattern=r"^KNW-[A-Z0-9]{3}-[A-Z0-9]{3}-[0-9]{3}$",
    )
    version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    building_type: str = Field(..., max_length=64)
    construction_phase: str = Field(..., max_length=64)
    construction_task: str = Field(..., max_length=128)
    knowledge_type: KnowledgeType
    status: KnowledgeStatus = "draft"
    risk_level: RiskLevel = "low"
    scope: Scope = "master"

    @field_validator("id")
    @classmethod
    def validate_no_path_traversal(cls, v):
        """Reject path traversal attempts."""
        if ".." in v or "/" in v or "\\" in v or "~" in v:
            raise ValueError("Path traversal characters not allowed in ID")
        return v


class KnowledgeRecord(BaseModel):
    """Complete knowledge record schema."""

    metadata: MetadataModel
    content: ContentModel
    source: SourceModel
    approval: ApprovalModel

    class Config:
        validate_assignment = True
        str_strip_whitespace = False  # Preserve intentional whitespace


def create_knowledge_record(
    knowledge_id: str,
    title: str,
    summary: str,
    knowledge_type: KnowledgeType,
    source_type: SourceType,
    building_type: str = "木造平屋",
    construction_phase: str = "基礎",
    construction_task: str = "基礎配筋",
    risk_level: RiskLevel = "low",
    created_by: str = "system",
) -> KnowledgeRecord:
    """Factory function to create knowledge record."""
    now = datetime.utcnow().isoformat() + "Z"

    return KnowledgeRecord(
        metadata=MetadataModel(
            id=knowledge_id,
            version="0.1.0",
            building_type=building_type,
            construction_phase=construction_phase,
            construction_task=construction_task,
            knowledge_type=knowledge_type,
            status="draft",
            risk_level=risk_level,
            scope="master",
        ),
        content=ContentModel(
            title=title,
            summary=summary,
            requirements=[],
            checks=[],
        ),
        source=SourceModel(
            primary_source_type=source_type,
            source_classification=source_type,
            sources=[],
            evidence_sufficiency="insufficient",
            evidence_notes="Draft created, evidence pending",
        ),
        approval=ApprovalModel(
            created_at=now,
            created_by=created_by,
            last_updated_at=now,
            last_updated_by=created_by,
            update_reason="Initial creation",
        ),
    )
