"""Evidence quality validation."""
from typing import Optional
from ..models import KnowledgeRecord, EvidenceSufficiency


class EvidenceValidator:
    """Validate evidence sufficiency and quality."""

    @staticmethod
    def check_evidence_sufficiency(record: KnowledgeRecord) -> tuple[bool, list[str]]:
        """Check if evidence meets sufficiency criteria.

        Returns: (is_sufficient, issues)
        """
        issues = []

        source = record.source
        if not source.sources:
            issues.append("No sources attached")
            return False, issues

        # Check: All sources have required fields
        for idx, src in enumerate(source.sources):
            if not src.title:
                issues.append(f"Source {idx}: Missing title")
            if not src.location:
                issues.append(f"Source {idx}: Missing location")
            if src.confidence_level == "low":
                issues.append(f"Source {idx}: Low confidence level")

        # Check: Evidence notes for gaps
        if source.evidence_notes and "gap" in source.evidence_notes.lower():
            issues.append("Evidence notes mention gaps")

        # Check: Source versions are specified
        for idx, src in enumerate(source.sources):
            if not src.version or src.version == "unknown":
                issues.append(f"Source {idx}: Version not specified")

        # Check: No contradictions (basic heuristic)
        if len(source.sources) > 1:
            has_high_confidence = any(s.confidence_level == "high" for s in source.sources)
            has_low_confidence = any(s.confidence_level == "low" for s in source.sources)
            if has_high_confidence and has_low_confidence:
                issues.append("Mixed confidence levels across sources")

        return len(issues) == 0, issues

    @staticmethod
    def validate_source_classification(
        record: KnowledgeRecord, allowed_classifications: Optional[list] = None
    ) -> tuple[bool, list[str]]:
        """Validate source classification rules.

        Returns: (is_valid, issues)
        """
        issues = []
        source = record.source

        if not source.primary_source_type:
            issues.append("primary_source_type not set")
            return False, issues

        # CRITICAL Rule: AI cannot unilaterally promote to company_standard
        # Check: primary_source_type is company_standard but created by AI
        ai_patterns = ["ai_", "ai-", "agent_", "agent-", "automation_", "automation-", "system_", "claude", "bot_"]
        is_ai_created = any(pattern in record.approval.created_by.lower() for pattern in ai_patterns)

        if source.primary_source_type == "company_standard" and is_ai_created:
            issues.append(
                "HUMAN_APPROVAL_REQUIRED: AI cannot unilaterally classify as company_standard; "
                "manager/director approval required"
            )

        # CRITICAL Rule: general_practice cannot be automatically promoted to company_standard
        # This must be explicit Human Decision
        if source.primary_source_type == "company_standard" and source.source_classification == "general_practice":
            issues.append(
                "USER_DECISION_REQUIRED: Promotion from general_practice to company_standard "
                "requires explicit human business decision (manager/director approval)"
            )

        # Classify restrictions
        if allowed_classifications:
            if source.source_classification not in allowed_classifications:
                issues.append(
                    f"source_classification '{source.source_classification}' "
                    f"not in allowed: {allowed_classifications}"
                )

        return len(issues) == 0, issues

    @staticmethod
    def require_exception_documentation(record: KnowledgeRecord) -> tuple[bool, str]:
        """Check if insufficient evidence requires exception documentation.

        Returns: (requires_exception, reason)
        """
        if record.source.evidence_sufficiency == "insufficient":
            if not record.source.evidence_notes:
                return True, "Insufficient evidence without exception documentation"
            if len(record.source.evidence_notes) < 50:
                return (
                    True,
                    "Insufficient evidence with inadequate exception documentation",
                )
            return False, ""

        return False, ""

    @staticmethod
    def assess_evidence_quality(record: KnowledgeRecord) -> dict:
        """Comprehensive evidence quality assessment.

        Returns: dict with quality metrics
        """
        source = record.source
        quality = {
            "total_sources": len(source.sources),
            "high_confidence_sources": sum(
                1 for s in source.sources if s.confidence_level == "high"
            ),
            "has_current_sources": any(
                s.accessed_at and int(s.accessed_at[:4]) >= 2024
                for s in source.sources
            ),
            "has_version_info": all(s.version and s.version != "unknown" for s in source.sources),
            "has_evidence_notes": bool(source.evidence_notes),
            "evidence_sufficiency": source.evidence_sufficiency,
            "issues": [],
        }

        if quality["total_sources"] == 0:
            quality["issues"].append("No sources")
        if quality["high_confidence_sources"] == 0:
            quality["issues"].append("No high-confidence sources")
        if not quality["has_current_sources"]:
            quality["issues"].append("No current sources (accessed in 2024+)")

        return quality
