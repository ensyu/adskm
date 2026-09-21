"""Knowledge-specific security validation (poisoning, integrity, contamination)."""
from typing import Optional
from ..models import KnowledgeRecord


class KnowledgeSecurityValidator:
    """Prevent knowledge poisoning, integrity attacks, and contamination."""

    @staticmethod
    def check_ai_hallucination_risk(record: KnowledgeRecord) -> tuple[bool, list[str]]:
        """Detect potential AI hallucination in source citations.

        Returns: (is_safe, concerns)
        """
        concerns = []

        if record.source.primary_source_type == "ai_structured":
            for idx, src in enumerate(record.source.sources):
                # AI-structured sources MUST have page references to cited material
                if not src.page_reference or src.page_reference == "unknown":
                    concerns.append(
                        f"AI-structured source {idx}: Missing page reference "
                        f"(cannot verify accuracy)"
                    )

                # Confidence must be explicit
                if src.confidence_level == "low":
                    concerns.append(
                        f"AI-structured source {idx}: Low confidence "
                        f"(hallucination risk)"
                    )

        return len(concerns) == 0, concerns

    @staticmethod
    def check_field_record_authenticity(record: KnowledgeRecord) -> tuple[bool, list[str]]:
        """Validate field_record observations for authenticity markers.

        Returns: (is_authentic, concerns)
        """
        concerns = []

        if record.source.primary_source_type == "field_record":
            for idx, src in enumerate(record.source.sources):
                # Field records MUST have observation metadata
                if not src.location or src.location == "unknown":
                    concerns.append(f"Field record {idx}: Missing observation location")

                if not src.accessed_at or src.accessed_at == "unknown":
                    concerns.append(f"Field record {idx}: Missing observation date")

                # Non-typical conditions should be flagged
                if src.title and ("unusual" in src.title.lower() or "exception" in src.title.lower()):
                    concerns.append(
                        f"Field record {idx}: Non-typical conditions noted "
                        f"(requires supervisor review)"
                    )

        return len(concerns) == 0, concerns

    @staticmethod
    def check_source_contradiction(record: KnowledgeRecord) -> tuple[bool, list[str]]:
        """Detect contradictions between evidence sources.

        Returns: (no_contradiction, conflicts)
        """
        conflicts = []

        # Check for obvious contradictions (naive heuristic)
        # Future: More sophisticated semantic analysis
        if len(record.source.sources) > 1:
            sources_text = [s.title.lower() for s in record.source.sources]

            # Simple pattern: if sources mention opposite requirements
            opposite_pairs = [
                ("required", "optional"),
                ("mandatory", "recommended"),
                ("prohibited", "allowed"),
            ]

            for word1, word2 in opposite_pairs:
                has_word1 = any(word1 in text for text in sources_text)
                has_word2 = any(word2 in text for text in sources_text)

                if has_word1 and has_word2:
                    conflicts.append(
                        f"Contradictory sources: '{word1}' vs '{word2}' detected"
                    )

        return len(conflicts) == 0, conflicts

    @staticmethod
    def check_approval_contamination(record: KnowledgeRecord) -> tuple[bool, list[str]]:
        """Detect signs of unapproved knowledge appearing as approved.

        Returns: (is_clean, concerns)
        """
        concerns = []

        # Rule: draft knowledge should not have approval_by set
        if record.metadata.status == "draft" and record.approval.approved_by:
            concerns.append(
                "Draft knowledge marked as approved (contamination risk)"
            )

        # Rule: Only humans can approve
        if (
            record.approval.approved_by
            and ("ai_" in record.approval.approved_by.lower()
                 or "agent" in record.approval.approved_by.lower())
        ):
            concerns.append("Knowledge approved by AI (approval contamination)")

        # Rule: Approve time must be after review time
        if (
            record.approval.reviewed_at
            and record.approval.approved_at
            and record.approval.approved_at < record.approval.reviewed_at
        ):
            concerns.append(
                "Approval timestamp before review (temporal anomaly)"
            )

        return len(concerns) == 0, concerns

    @staticmethod
    def check_knowledge_aging(record: KnowledgeRecord) -> tuple[bool, str]:
        """Check if knowledge sources are becoming stale.

        Returns: (is_current, age_assessment)
        """
        from datetime import datetime

        now = datetime.utcnow()
        max_age_years = 2

        if record.source.sources:
            # Get newest source
            newest_accessed = max(
                s.accessed_at for s in record.source.sources if s.accessed_at
            )
            accessed_year = int(newest_accessed[:4])
            current_year = now.year
            age = current_year - accessed_year

            if age > max_age_years:
                return (
                    False,
                    f"Newest source is {age} years old (accessed {accessed_year}); "
                    f"recommend review",
                )

        return True, "Sources current"

    @staticmethod
    def comprehensive_knowledge_security_check(
        record: KnowledgeRecord,
    ) -> dict:
        """Comprehensive security assessment across all knowledge threats.

        Returns: dict with all security checks
        """
        hallucination_safe, hallucination_concerns = (
            KnowledgeSecurityValidator.check_ai_hallucination_risk(record)
        )
        authenticity_safe, authenticity_concerns = (
            KnowledgeSecurityValidator.check_field_record_authenticity(record)
        )
        no_contradiction, contradiction_conflicts = (
            KnowledgeSecurityValidator.check_source_contradiction(record)
        )
        approval_clean, approval_concerns = (
            KnowledgeSecurityValidator.check_approval_contamination(record)
        )
        sources_current, aging_assessment = (
            KnowledgeSecurityValidator.check_knowledge_aging(record)
        )

        all_passed = (
            hallucination_safe
            and authenticity_safe
            and no_contradiction
            and approval_clean
            and sources_current
        )

        return {
            "passed": all_passed,
            "hallucination": {"passed": hallucination_safe, "concerns": hallucination_concerns},
            "authenticity": {"passed": authenticity_safe, "concerns": authenticity_concerns},
            "contradiction": {"passed": no_contradiction, "conflicts": contradiction_conflicts},
            "approval": {"passed": approval_clean, "concerns": approval_concerns},
            "aging": {"passed": sources_current, "assessment": aging_assessment},
            "overall_concerns": (
                hallucination_concerns + authenticity_concerns +
                contradiction_conflicts + approval_concerns
            ),
        }
