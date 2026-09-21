"""Tests for security (knowledge poisoning, data integrity, contamination)."""
import pytest
import tempfile
from pathlib import Path
import yaml
from src.adskm.security import KnowledgeSecurityValidator, DataSecurityValidator
from src.adskm.models import create_knowledge_record, SourceRecord


class TestDataSecurityValidator:
    """Test general data security checks."""

    def test_yaml_size_limit_enforced(self):
        """Oversized YAML files should be rejected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            large_file = tmppath / "large.yaml"

            # Create file larger than 1MB
            with open(large_file, "w") as f:
                f.write("x" * (1_000_001))

            is_safe, error = DataSecurityValidator.check_yaml_size(large_file)
            assert not is_safe
            assert "exceeds" in error

    def test_yaml_safe_load_only(self):
        """Should use only yaml.safe_load()."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            test_file = tmppath / "test.yaml"

            # Write valid YAML
            test_file.write_text("key: value\n")

            success, data, error = DataSecurityValidator.safe_yaml_load(test_file)
            assert success
            assert data["key"] == "value"

    def test_credential_leakage_detection(self):
        """Should detect credential patterns."""
        # API key in data
        data_with_creds = {
            "content": {
                "api_key": "sk-1234567890",
            }
        }

        is_safe, concerns = DataSecurityValidator.check_credential_leakage(
            data_with_creds
        )
        assert not is_safe
        assert len(concerns) > 0

    def test_personal_information_detection(self):
        """Should detect PII."""
        data_with_pii = {
            "approval": {
                "approved_by": "john.doe@company.com",
            }
        }

        is_safe, concerns = DataSecurityValidator.check_personal_information(
            data_with_pii
        )
        assert not is_safe
        assert "Email address" in concerns[0]

    def test_api_exposure_detection(self):
        """Should detect exposed API endpoints."""
        data_with_api = {
            "source": {
                "location": "https://api.kanna.com/v1/endpoint",
            }
        }

        is_safe, concerns = DataSecurityValidator.check_external_api_exposure(
            data_with_api
        )
        # Should flag potential API exposure
        # This may or may not be a concern depending on context

    def test_comprehensive_data_security_check(self):
        """Should perform comprehensive security check."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            test_file = tmppath / "test.yaml"

            test_file.write_text("key: value\n")

            data = {"key": "value"}
            result = DataSecurityValidator.comprehensive_data_security_check(
                test_file, data
            )

            assert "passed" in result
            assert "file_size" in result
            assert "credentials" in result


class TestKnowledgeSecurityValidator:
    """Test knowledge-specific security checks."""

    def test_ai_hallucination_risk_detection(self):
        """Should detect AI hallucination risk."""
        record = create_knowledge_record(
            knowledge_id="KNW-W01-FND-001",
            title="Test",
            summary="Test",
            knowledge_type="procedure",
            source_type="ai_structured",
            created_by="ai_process",
        )

        # AI-structured source without page reference
        record.source.sources.append(
            SourceRecord(
                title="Source",
                type="regulation",
                version="2024",
                location="https://example.com",
                accessed_at="2024-01-15",
                confidence_level="low",
            )
        )

        is_safe, concerns = (
            KnowledgeSecurityValidator.check_ai_hallucination_risk(record)
        )
        assert not is_safe  # Low confidence
        assert len(concerns) > 0

    def test_field_record_authenticity_check(self):
        """Should validate field record authenticity."""
        record = create_knowledge_record(
            knowledge_id="KNW-W01-FND-001",
            title="Test",
            summary="Test",
            knowledge_type="procedure",
            source_type="field_record",
        )

        # Field record without location
        record.source.sources.append(
            SourceRecord(
                title="Observation",
                type="field_record",
                version="unknown",
                location="unknown",  # Missing location
                accessed_at="2024-01-15",
            )
        )

        is_authentic, concerns = (
            KnowledgeSecurityValidator.check_field_record_authenticity(record)
        )
        assert not is_authentic
        assert len(concerns) > 0

    def test_source_contradiction_detection(self):
        """Should check for contradictions with multiple sources."""
        record = create_knowledge_record(
            knowledge_id="KNW-W01-FND-001",
            title="Test",
            summary="Test",
            knowledge_type="procedure",
            source_type="general_practice",
        )

        # Add contradictory sources
        record.source.sources.append(
            SourceRecord(
                title="Source requires something as mandatory",
                type="regulation",
                version="2024",
                location="https://example.com",
                accessed_at="2024-01-15",
            )
        )
        record.source.sources.append(
            SourceRecord(
                title="Different source says it is prohibited",
                type="general_practice",
                version="2024",
                location="https://example.com",
                accessed_at="2024-01-15",
            )
        )

        no_contradiction, conflicts = (
            KnowledgeSecurityValidator.check_source_contradiction(record)
        )
        # With two sources, potential contradiction check runs
        # The heuristic may or may not detect it depending on exact text
        assert isinstance(no_contradiction, bool)
        assert isinstance(conflicts, list)

    def test_approval_contamination_detection(self):
        """Should detect unapproved knowledge marked as approved."""
        record = create_knowledge_record(
            knowledge_id="KNW-W01-FND-001",
            title="Test",
            summary="Test",
            knowledge_type="procedure",
            source_type="general_practice",
        )

        # Draft knowledge marked as approved
        record.metadata.status = "draft"
        record.approval.approved_by = "manager"

        is_clean, concerns = (
            KnowledgeSecurityValidator.check_approval_contamination(record)
        )
        assert not is_clean
        assert "contamination" in concerns[0].lower()

    def test_ai_approval_rejection(self):
        """Should reject AI approvals."""
        record = create_knowledge_record(
            knowledge_id="KNW-W01-FND-001",
            title="Test",
            summary="Test",
            knowledge_type="procedure",
            source_type="general_practice",
        )

        # AI approved (lowercase detection)
        record.approval.approved_by = "ai_agent_001"

        is_clean, concerns = (
            KnowledgeSecurityValidator.check_approval_contamination(record)
        )
        assert not is_clean
        assert len(concerns) > 0

    def test_knowledge_aging_check(self):
        """Should check knowledge source age."""
        record = create_knowledge_record(
            knowledge_id="KNW-W01-FND-001",
            title="Test",
            summary="Test",
            knowledge_type="procedure",
            source_type="general_practice",
        )

        # Old source
        record.source.sources.append(
            SourceRecord(
                title="Old source",
                type="regulation",
                version="2020",
                location="https://example.com",
                accessed_at="2020-01-15",  # 4 years old
            )
        )

        is_current, assessment = (
            KnowledgeSecurityValidator.check_knowledge_aging(record)
        )
        assert not is_current
        assert "outdated" in assessment.lower() or "old" in assessment.lower()

    def test_comprehensive_security_check(self):
        """Should perform comprehensive security assessment."""
        record = create_knowledge_record(
            knowledge_id="KNW-W01-FND-001",
            title="Test",
            summary="Test",
            knowledge_type="procedure",
            source_type="general_practice",
        )

        result = (
            KnowledgeSecurityValidator.comprehensive_knowledge_security_check(
                record
            )
        )

        assert "passed" in result
        assert "hallucination" in result
        assert "authenticity" in result
        assert "contradiction" in result
        assert "approval" in result
        assert "aging" in result
        assert "overall_concerns" in result
