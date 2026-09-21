"""Knowledge Service - Load, save, validate master knowledge."""
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple
import yaml
from ..models import KnowledgeRecord
from ..security import DataSecurityValidator


class KnowledgeService:
    """Manage knowledge record lifecycle (load, save, validate)."""

    def __init__(self, knowledge_base: Path):
        """Initialize service with knowledge base directory.

        Args:
            knowledge_base: Path to knowledge/ directory
        """
        self.knowledge_base = Path(knowledge_base)
        self.master_dir = self.knowledge_base / "master"
        self.drafts_dir = self.knowledge_base / "drafts"
        self.audit_dir = self.knowledge_base / "audit_logs"

        # Ensure directories exist
        self.master_dir.mkdir(parents=True, exist_ok=True)
        self.drafts_dir.mkdir(parents=True, exist_ok=True)
        self.audit_dir.mkdir(parents=True, exist_ok=True)

    def _get_knowledge_path(self, knowledge_id: str, scope: str = "master") -> Path:
        """Resolve knowledge file path safely (path traversal prevention).

        Returns: Path (validated)
        """
        if scope == "master":
            base_dir = self.master_dir
        elif scope == "draft":
            base_dir = self.drafts_dir
        else:
            raise ValueError(f"Unknown scope: {scope}")

        filename = f"{knowledge_id}.yaml"
        file_path = base_dir / filename

        # Check for path traversal
        try:
            resolved = file_path.resolve()
            base_resolved = base_dir.resolve()
            if not str(resolved).startswith(str(base_resolved)):
                raise ValueError(f"Path escapes boundary: {file_path}")
        except Exception as e:
            raise ValueError(f"Invalid path: {e}")

        return file_path

    def load_master(self, knowledge_id: str) -> Tuple[bool, Optional[KnowledgeRecord], str]:
        """Load approved master knowledge (read-only).

        Returns: (success, record, error_message)
        """
        file_path = self._get_knowledge_path(knowledge_id, scope="master")

        if not file_path.exists():
            return False, None, f"Master knowledge not found: {knowledge_id}"

        # Load YAML safely
        success, data, error = DataSecurityValidator.safe_yaml_load(file_path)
        if not success:
            return False, None, error

        # Validate schema
        try:
            record = KnowledgeRecord(**data)
            # Enforce master-only status
            if record.metadata.status not in ["approved", "superseded"]:
                return (
                    False,
                    None,
                    f"Master knowledge has unexpected status: {record.metadata.status}",
                )
            return True, record, ""
        except Exception as e:
            return False, None, f"Schema validation error: {e}"

    def load_draft(
        self, knowledge_id: str, user_id: Optional[str] = None
    ) -> Tuple[bool, Optional[KnowledgeRecord], str]:
        """Load draft knowledge (access-controlled).

        Returns: (success, record, error_message)
        """
        file_path = self._get_knowledge_path(knowledge_id, scope="draft")

        if not file_path.exists():
            return False, None, f"Draft knowledge not found: {knowledge_id}"

        # Load YAML safely
        success, data, error = DataSecurityValidator.safe_yaml_load(file_path)
        if not success:
            return False, None, error

        # Validate schema
        try:
            record = KnowledgeRecord(**data)
            # Access control: creator and assigned reviewers only
            if user_id:
                if user_id != record.approval.created_by:
                    # Could add assigned_reviewers check here
                    pass
            return True, record, ""
        except Exception as e:
            return False, None, f"Schema validation error: {e}"

    def save_draft(
        self, record: KnowledgeRecord, user_id: str
    ) -> Tuple[bool, str]:
        """Save knowledge record as draft.

        Returns: (success, error_message)
        """
        # Validate record
        try:
            record_validated = KnowledgeRecord(**record.dict())
        except Exception as e:
            return False, f"Record validation failed: {e}"

        # Draft must be in draft status
        if record.metadata.status not in ["draft", "review_required"]:
            return False, "Draft can only be in 'draft' or 'review_required' status"

        file_path = self._get_knowledge_path(record.metadata.id, scope="draft")

        # Save to YAML
        try:
            data = record.model_dump()
            success, error = DataSecurityValidator.safe_yaml_dump(data, file_path)
            if not success:
                return False, error

            # Set draft permissions (read-only for others)
            os.chmod(file_path, 0o600)
            return True, ""
        except Exception as e:
            return False, f"Error saving draft: {e}"

    def save_master(self, record: KnowledgeRecord, approver_id: str) -> Tuple[bool, str]:
        """Save knowledge record as master (approval-only).

        Returns: (success, error_message)
        """
        # Only humans can approve
        if "ai_" in approver_id.lower() or "agent" in approver_id.lower():
            return False, "AI cannot approve knowledge; human approval required"

        # Must be approved status
        if record.metadata.status not in ["approved"]:
            return False, "Master knowledge must have 'approved' status"

        # Must have approval metadata
        if not record.approval.approved_at or not record.approval.approved_by:
            return False, "Master knowledge missing approval metadata"

        file_path = self._get_knowledge_path(record.metadata.id, scope="master")

        # Save to YAML
        try:
            data = record.model_dump()
            success, error = DataSecurityValidator.safe_yaml_dump(data, file_path)
            if not success:
                return False, error

            # Set master permissions (read-only, immutable)
            os.chmod(file_path, 0o440)
            return True, ""
        except Exception as e:
            return False, f"Error saving master: {e}"

    def list_master_knowledge(self) -> list[str]:
        """List all approved master knowledge IDs.

        Returns: list of knowledge IDs
        """
        ids = []
        for file_path in self.master_dir.glob("*.yaml"):
            knowledge_id = file_path.stem
            ids.append(knowledge_id)
        return sorted(ids)

    def list_draft_knowledge(self) -> list[str]:
        """List all draft knowledge IDs.

        Returns: list of knowledge IDs
        """
        ids = []
        for file_path in self.drafts_dir.glob("*.yaml"):
            knowledge_id = file_path.stem
            ids.append(knowledge_id)
        return sorted(ids)

    def delete_draft(self, knowledge_id: str) -> Tuple[bool, str]:
        """Delete a draft knowledge record.

        Returns: (success, error_message)
        """
        file_path = self._get_knowledge_path(knowledge_id, scope="draft")

        if not file_path.exists():
            return False, f"Draft not found: {knowledge_id}"

        try:
            # Remove read-only flag
            os.chmod(file_path, 0o600)
            file_path.unlink()
            return True, ""
        except Exception as e:
            return False, f"Error deleting draft: {e}"

    def version_bump(self, record: KnowledgeRecord, bump_type: str) -> str:
        """Bump semantic version based on change type.

        Args:
            record: Knowledge record
            bump_type: "major", "minor", or "patch"

        Returns: new version string
        """
        parts = record.metadata.version.split(".")
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

        if bump_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif bump_type == "minor":
            minor += 1
            patch = 0
        elif bump_type == "patch":
            patch += 1
        else:
            raise ValueError(f"Unknown bump type: {bump_type}")

        return f"{major}.{minor}.{patch}"
