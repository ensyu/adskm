"""Project Override Schema (Project-specific knowledge exceptions)."""
from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict
from .knowledge import (
    ContentModel,
    SourceModel,
    ApprovalModel,
    RiskLevel,
    KnowledgeType,
)


class OverrideMetadataModel(BaseModel):
    """Project override metadata."""

    id: str = Field(
        ...,
        pattern=r"^KNW-[A-Z0-9]{3}-[A-Z0-9]{3}-[0-9]{3}$",
    )
    version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    project_id: str = Field(..., max_length=128)
    scope: Literal["project_override"] = "project_override"
    risk_level: RiskLevel = "low"
    knowledge_type: KnowledgeType = "procedure"


class ProjectOverride(BaseModel):
    """Project-specific override (isolated from master knowledge)."""

    model_config = ConfigDict(validate_assignment=True)

    metadata: OverrideMetadataModel
    content: ContentModel
    source: SourceModel
    approval: ApprovalModel
    master_id: str = Field(
        ...,
        pattern=r"^KNW-[A-Z0-9]{3}-[A-Z0-9]{3}-[0-9]{3}$",
    )


def create_project_override(
    knowledge_id: str,
    project_id: str,
    title: str,
    summary: str,
    knowledge_type: KnowledgeType = "procedure",
    risk_level: RiskLevel = "low",
    created_by: str = "system",
) -> ProjectOverride:
    """Factory function to create project override."""
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    return ProjectOverride(
        metadata=OverrideMetadataModel(
            id=knowledge_id,
            version="0.1.0",
            project_id=project_id,
            risk_level=risk_level,
            knowledge_type=knowledge_type,
        ),
        content=ContentModel(
            title=title,
            summary=summary,
            requirements=[],
            checks=[],
        ),
        source=SourceModel(
            primary_source_type="field_record",
            source_classification="field_record",
            sources=[],
            evidence_sufficiency="insufficient",
            evidence_notes="Project-specific override, evidence pending",
        ),
        approval=ApprovalModel(
            created_at=now,
            created_by=created_by,
            last_updated_at=now,
            last_updated_by=created_by,
            update_reason="Project override creation",
        ),
        master_id=knowledge_id,
    )
