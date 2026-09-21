"""Script to create sample knowledge record for demonstration."""
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.adskm.models import (
    create_knowledge_record,
    SourceRecord,
)
from src.adskm.services import KnowledgeService


def create_foundation_knowledge():
    """Create KNW-W01-FND-001: Foundation Reinforcement Standard."""

    # Create knowledge record
    record = create_knowledge_record(
        knowledge_id="KNW-W01-FND-001",
        title="Foundation Reinforcement Spacing Standard (木造平屋基礎配筋)",
        summary="Company standard for reinforcement spacing in single-story wooden building foundations",
        knowledge_type="specification",
        source_type="general_practice",
        created_by="adskm_system",
    )

    # Update to draft status
    record.metadata.status = "draft"

    # Add content
    record.content.requirements = [
        "Reinforcement spacing: 200mm centers (standard)",
        "Bar diameter: D13 minimum for main reinforcement",
        "Concrete cover: 50mm minimum (exposed)",
        "Lap splice: 40 bar diameters (D13 = 520mm minimum)",
        "Stirrups: D10 @ 150mm centers",
    ]

    record.content.checks = [
        "Verify spacing with site measurement",
        "Check bar diameter labels on delivery",
        "Inspect concrete cover with depth gauge",
        "Review lap splice lengths before placement",
        "Photograph stirrup arrangement",
    ]

    # Add evidence sources
    now = datetime.utcnow().isoformat() + "Z"

    # Source 1: Building Standard Code
    record.source.sources.append(
        SourceRecord(
            title="日本建築学会 木造建築工事標準仕様書 2022版",
            type="approved_procedure",
            version="2022",
            location="https://www.aij.or.jp/",
            page_reference="pp. 234-240",
            accessed_at="2024-09-01",
            confidence_level="high",
        )
    )

    # Source 2: Field Records
    record.source.sources.append(
        SourceRecord(
            title="Project ABC Foundation Inspection Report",
            type="field_record",
            version="1.0",
            location="file:///projects/abc/inspection_2024.pdf",
            page_reference="Appendix A",
            accessed_at="2024-08-15",
            confidence_level="high",
        )
    )

    # Update evidence status
    record.source.evidence_sufficiency = "sufficient"
    record.source.evidence_notes = (
        "Standards based on AIJ 2022 specification. "
        "Field validation from Project ABC foundation inspection confirms "
        "spacing practice aligns with specification. "
        "No contradictions between sources. "
        "Ready for review."
    )

    # Update approval metadata
    record.approval.last_updated_at = now
    record.approval.update_reason = "Initial draft creation with evidence"

    return record


def main():
    """Save sample knowledge record."""
    knowledge_base = Path(__file__).parent.parent / "knowledge"
    service = KnowledgeService(knowledge_base)

    record = create_foundation_knowledge()

    # Save as draft
    success, error = service.save_draft(record, user_id="adskm_system")

    if success:
        print(f"✅ Created draft knowledge: {record.metadata.id}")
        print(f"   Status: {record.metadata.status}")
        print(f"   Version: {record.metadata.version}")
        print(f"   Sources: {len(record.source.sources)}")
        print(f"   Evidence: {record.source.evidence_sufficiency}")
        return 0
    else:
        print(f"❌ Failed to create knowledge: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
