"""Tests for services (Knowledge, Audit, Override)."""
import pytest
import tempfile
from pathlib import Path
from datetime import datetime
from src.adskm.services import KnowledgeService, AuditService, OverrideService
from src.adskm.models import (
    create_knowledge_record,
    AuditEntry,
    ProjectOverride,
)


@pytest.fixture
def temp_knowledge_dir():
    """Create temporary knowledge directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestKnowledgeService:
    """Test KnowledgeService YAML operations."""

    def test_service_initialization(self, temp_knowledge_dir):
        """Service should initialize directories."""
        service = KnowledgeService(temp_knowledge_dir)
        assert service.master_dir.exists()
        assert service.drafts_dir.exists()
        assert service.audit_dir.exists()

    def test_save_and_load_draft(self, temp_knowledge_dir):
        """Should save and load draft knowledge."""
        service = KnowledgeService(temp_knowledge_dir)
        record = create_knowledge_record(
            knowledge_id="KNW-W01-FND-001",
            title="Test Knowledge",
            summary="Test summary",
            knowledge_type="procedure",
            source_type="general_practice",
        )

        # Save draft
        success, error = service.save_draft(record, user_id="test_user")
        assert success, f"Save failed: {error}"

        # Load draft
        success, loaded, error = service.load_draft("KNW-W01-FND-001")
        assert success, f"Load failed: {error}"
        assert loaded.metadata.id == "KNW-W01-FND-001"

    def test_path_traversal_prevention(self, temp_knowledge_dir):
        """Path traversal attempts should be rejected."""
        service = KnowledgeService(temp_knowledge_dir)

        with pytest.raises(ValueError, match="Path escapes boundary"):
            service._get_knowledge_path("../../../etc/passwd", scope="master")

    def test_list_master_knowledge(self, temp_knowledge_dir):
        """Should list master knowledge."""
        service = KnowledgeService(temp_knowledge_dir)

        record1 = create_knowledge_record(
            knowledge_id="KNW-W01-FND-001",
            title="Knowledge 1",
            summary="Summary 1",
            knowledge_type="procedure",
            source_type="general_practice",
        )
        record1.metadata.status = "approved"
        record1.approval.approved_at = datetime.utcnow().isoformat() + "Z"
        record1.approval.approved_by = "manager"

        success, error = service.save_master(record1, approver_id="manager")
        assert success

        ids = service.list_master_knowledge()
        assert "KNW-W01-FND-001" in ids

    def test_version_bump_patch(self, temp_knowledge_dir):
        """Should bump patch version."""
        service = KnowledgeService(temp_knowledge_dir)
        record = create_knowledge_record(
            knowledge_id="KNW-W01-FND-001",
            title="Test",
            summary="Test",
            knowledge_type="procedure",
            source_type="general_practice",
        )

        new_version = service.version_bump(record, "patch")
        assert new_version == "0.1.1"

    def test_version_bump_minor(self, temp_knowledge_dir):
        """Should bump minor version."""
        service = KnowledgeService(temp_knowledge_dir)
        record = create_knowledge_record(
            knowledge_id="KNW-W01-FND-001",
            title="Test",
            summary="Test",
            knowledge_type="procedure",
            source_type="general_practice",
        )

        new_version = service.version_bump(record, "minor")
        assert new_version == "0.2.0"

    def test_version_bump_major(self, temp_knowledge_dir):
        """Should bump major version."""
        service = KnowledgeService(temp_knowledge_dir)
        record = create_knowledge_record(
            knowledge_id="KNW-W01-FND-001",
            title="Test",
            summary="Test",
            knowledge_type="procedure",
            source_type="general_practice",
        )

        new_version = service.version_bump(record, "major")
        assert new_version == "1.0.0"

    def test_ai_cannot_approve(self, temp_knowledge_dir):
        """AI should not be able to approve knowledge."""
        service = KnowledgeService(temp_knowledge_dir)
        record = create_knowledge_record(
            knowledge_id="KNW-W01-FND-001",
            title="Test",
            summary="Test",
            knowledge_type="procedure",
            source_type="general_practice",
        )
        record.metadata.status = "approved"
        record.approval.approved_at = datetime.utcnow().isoformat() + "Z"
        record.approval.approved_by = "AI_Agent_001"

        success, error = service.save_master(record, approver_id="ai_process")
        assert not success, "AI should not be able to approve"


class TestAuditService:
    """Test AuditService append-only logging."""

    def test_audit_service_initialization(self, temp_knowledge_dir):
        """Service should initialize audit directory."""
        service = AuditService(temp_knowledge_dir / "audit_logs")
        assert service.audit_dir.exists()
        assert service.archive_dir.exists()

    def test_append_audit_entry(self, temp_knowledge_dir):
        """Should append audit entry."""
        service = AuditService(temp_knowledge_dir / "audit_logs")
        entry = AuditEntry(
            timestamp="2024-01-15T10:00:00Z",
            change_id="AUD-001",
            who="reviewer",
            action="create",
            knowledge_id="KNW-W01-FND-001",
            new_version="0.1.0",
            new_status="draft",
        )

        success, error = service.append_entry(entry)
        assert success, f"Append failed: {error}"

    def test_read_audit_entries(self, temp_knowledge_dir):
        """Should read all audit entries."""
        service = AuditService(temp_knowledge_dir / "audit_logs")

        entry1 = AuditEntry(
            timestamp="2024-01-15T10:00:00Z",
            change_id="AUD-001",
            who="reviewer",
            action="create",
            knowledge_id="KNW-W01-FND-001",
            new_version="0.1.0",
            new_status="draft",
        )
        entry2 = AuditEntry(
            timestamp="2024-01-15T11:00:00Z",
            change_id="AUD-002",
            who="reviewer",
            action="update",
            knowledge_id="KNW-W01-FND-001",
            new_version="0.2.0",
            new_status="review_required",
        )

        service.append_entry(entry1)
        service.append_entry(entry2)

        success, entries, error = service.read_all_entries()
        assert success
        assert len(entries) >= 2

    def test_query_audit_entries(self, temp_knowledge_dir):
        """Should query audit entries by knowledge_id."""
        service = AuditService(temp_knowledge_dir / "audit_logs")

        entry = AuditEntry(
            timestamp="2024-01-15T10:00:00Z",
            change_id="AUD-001",
            who="reviewer",
            action="create",
            knowledge_id="KNW-W01-FND-001",
            new_version="0.1.0",
            new_status="draft",
        )
        service.append_entry(entry)

        success, entries, error = service.query_entries(
            knowledge_id="KNW-W01-FND-001"
        )
        assert success
        assert len(entries) > 0


class TestOverrideService:
    """Test OverrideService project overrides."""

    def test_override_service_initialization(self, temp_knowledge_dir):
        """Service should initialize overrides directory."""
        service = OverrideService(temp_knowledge_dir)
        assert service.overrides_dir.exists()

    def test_save_and_load_override(self, temp_knowledge_dir):
        """Should save and load project override."""
        service = OverrideService(temp_knowledge_dir)

        from src.adskm.models import (
            OverrideMetadataModel,
            ContentModel,
            SourceModel,
            ApprovalModel,
        )

        now = datetime.utcnow().isoformat() + "Z"
        override = ProjectOverride(
            metadata=OverrideMetadataModel(
                id="KNW-W01-FND-001",
                version="0.1.0",
                project_id="PROJECT_X",
            ),
            content=ContentModel(
                title="Project Override",
                summary="Project-specific requirements",
            ),
            source=SourceModel(
                primary_source_type="field_record",
                source_classification="field_record",
            ),
            approval=ApprovalModel(
                created_at=now,
                created_by="project_manager",
                last_updated_at=now,
                last_updated_by="project_manager",
            ),
            master_id="KNW-W01-FND-001",
        )

        # Save
        success, error = service.save_override(override, "PROJECT_X")
        assert success, f"Save failed: {error}"

        # Load
        success, loaded, error = service.load_override(
            "KNW-W01-FND-001", "PROJECT_X"
        )
        assert success, f"Load failed: {error}"
        assert loaded.master_id == "KNW-W01-FND-001"

    def test_list_project_overrides(self, temp_knowledge_dir):
        """Should list project overrides."""
        service = OverrideService(temp_knowledge_dir)

        from src.adskm.models import (
            OverrideMetadataModel,
            ContentModel,
            SourceModel,
            ApprovalModel,
        )

        now = datetime.utcnow().isoformat() + "Z"
        override = ProjectOverride(
            metadata=OverrideMetadataModel(
                id="KNW-W01-FND-001",
                version="0.1.0",
                project_id="PROJECT_X",
            ),
            content=ContentModel(
                title="Override",
                summary="Summary",
            ),
            source=SourceModel(
                primary_source_type="field_record",
                source_classification="field_record",
            ),
            approval=ApprovalModel(
                created_at=now,
                created_by="pm",
                last_updated_at=now,
                last_updated_by="pm",
            ),
            master_id="KNW-W01-FND-001",
        )

        service.save_override(override, "PROJECT_X")

        ids = service.list_overrides_for_project("PROJECT_X")
        assert "KNW-W01-FND-001" in ids
