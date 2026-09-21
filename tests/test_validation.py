"""Tests for validation (schema, evidence, path safety)."""
import pytest
from pathlib import Path
from src.adskm.validation import EvidenceValidator, SchemaValidator
from src.adskm.models import (
    create_knowledge_record,
    SourceRecord,
)


class TestSchemaValidator:
    """Test schema validation."""

    def test_valid_knowledge_id_format(self):
        """Valid knowledge ID should pass."""
        is_valid, error = SchemaValidator.validate_knowledge_id_format(
            "KNW-W01-FND-001"
        )
        assert is_valid

    def test_invalid_knowledge_id_format(self):
        """Invalid knowledge ID should fail."""
        is_valid, error = SchemaValidator.validate_knowledge_id_format(
            "INVALID-ID"
        )
        assert not is_valid

    def test_path_traversal_detection(self):
        """Path traversal patterns should be detected."""
        # Test: ..
        is_safe, error = SchemaValidator.validate_no_path_traversal("../etc")
        assert not is_safe

        # Test: /
        is_safe, error = SchemaValidator.validate_no_path_traversal("home/user")
        assert not is_safe

        # Test: \
        is_safe, error = SchemaValidator.validate_no_path_traversal("windows\\path")
        assert not is_safe

        # Test: ~
        is_safe, error = SchemaValidator.validate_no_path_traversal("~/.bashrc")
        assert not is_safe

    def test_safe_path_component(self):
        """Safe path components should pass."""
        is_safe, error = SchemaValidator.validate_no_path_traversal("W01")
        assert is_safe

    def test_version_format_validation(self):
        """Valid semantic version should pass."""
        is_valid, error = SchemaValidator.validate_version_format("1.2.3")
        assert is_valid

    def test_invalid_version_format(self):
        """Invalid version format should fail."""
        is_valid, error = SchemaValidator.validate_version_format("1.2")
        assert not is_valid

    def test_iso8601_datetime_validation(self):
        """Valid ISO 8601 datetime should pass."""
        is_valid, error = SchemaValidator.validate_iso8601_datetime(
            "2024-01-15T10:00:00Z"
        )
        assert is_valid

    def test_invalid_iso8601_datetime(self):
        """Invalid datetime should fail."""
        is_valid, error = SchemaValidator.validate_iso8601_datetime(
            "2024-01-15 10:00:00"
        )
        assert not is_valid

    def test_field_length_limits(self):
        """Fields exceeding length limits should fail."""
        record_dict = {
            "metadata": {
                "id": "KNW-W01-FND-001",
                "building_type": "x" * 65,  # Exceeds 64 char limit
            },
            "content": {
                "title": "x" * 101,  # Exceeds 100 char limit
            },
        }
        is_valid, violations = SchemaValidator.validate_field_length_limits(
            record_dict
        )
        assert not is_valid
        assert len(violations) > 0


class TestPathSafety:
    """Test path traversal prevention."""

    def test_symlink_detection(self):
        """Symlinks should be detected."""
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)

            # Create a file
            target_file = base / "target.txt"
            target_file.write_text("content")

            # Create a symlink (if supported on platform)
            symlink_path = base / "symlink.txt"
            try:
                os.symlink(target_file, symlink_path)

                is_safe, error = SchemaValidator.check_symlink_safety(symlink_path)
                assert not is_safe
            except (OSError, NotImplementedError):
                # Skip on systems that don't support symlinks
                pytest.skip("Symlinks not supported on this system")

    def test_path_boundary_check(self):
        """Paths should stay within boundary."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir) / "knowledge"
            base.mkdir()

            # In-boundary path
            in_path = base / "record.yaml"
            is_safe, error = SchemaValidator.check_path_boundary(in_path, base)
            assert is_safe

            # Out-of-boundary path
            out_path = Path(tmpdir) / "../../etc/passwd"
            is_safe, error = SchemaValidator.check_path_boundary(out_path, base)
            assert not is_safe


class TestEvidenceValidator:
    """Test evidence quality validation."""

    def test_evidence_sufficiency_check(self):
        """Should check evidence sufficiency."""
        record = create_knowledge_record(
            knowledge_id="KNW-W01-FND-001",
            title="Test",
            summary="Test",
            knowledge_type="procedure",
            source_type="general_practice",
        )

        is_sufficient, issues = EvidenceValidator.check_evidence_sufficiency(
            record
        )
        assert not is_sufficient  # No sources added
        assert len(issues) > 0

    def test_evidence_with_sources(self):
        """Evidence with sources should check."""
        record = create_knowledge_record(
            knowledge_id="KNW-W01-FND-001",
            title="Test",
            summary="Test",
            knowledge_type="procedure",
            source_type="general_practice",
        )

        # Add a source
        record.source.sources.append(
            SourceRecord(
                title="Building Code 2024",
                type="regulation",
                version="2024",
                location="https://www.mlit.go.jp/code",
                accessed_at="2024-01-15",
                confidence_level="high",
            )
        )
        record.source.evidence_sufficiency = "sufficient"

        is_sufficient, issues = EvidenceValidator.check_evidence_sufficiency(
            record
        )
        assert is_sufficient or len(issues) == 0

    def test_source_classification_validation(self):
        """Should validate source classification rules."""
        record = create_knowledge_record(
            knowledge_id="KNW-W01-FND-001",
            title="Test",
            summary="Test",
            knowledge_type="procedure",
            source_type="company_standard",
        )
        # created_by must contain "ai_" in lowercase for the check
        record.approval.created_by = "ai_structured_process"

        is_valid, issues = EvidenceValidator.validate_source_classification(record)
        assert not is_valid  # AI cannot unilaterally classify as company_standard

    def test_evidence_quality_assessment(self):
        """Should assess evidence quality comprehensively."""
        record = create_knowledge_record(
            knowledge_id="KNW-W01-FND-001",
            title="Test",
            summary="Test",
            knowledge_type="procedure",
            source_type="general_practice",
        )

        record.source.sources.append(
            SourceRecord(
                title="Source",
                type="regulation",
                version="2024",
                location="https://example.com",
                accessed_at="2024-01-15",
                confidence_level="high",
            )
        )

        quality = EvidenceValidator.assess_evidence_quality(record)
        assert quality["total_sources"] == 1
        assert quality["high_confidence_sources"] == 1
