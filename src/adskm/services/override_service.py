"""Override Service - Project-specific knowledge overrides."""
import os
from pathlib import Path
from typing import Optional, Tuple
from ..models import ProjectOverride, KnowledgeRecord
from ..security import DataSecurityValidator


class OverrideService:
    """Manage project-specific knowledge overrides (isolated from master)."""

    def __init__(self, knowledge_base: Path):
        """Initialize service with knowledge base directory.

        Args:
            knowledge_base: Path to knowledge/ directory
        """
        self.knowledge_base = Path(knowledge_base)
        self.overrides_dir = self.knowledge_base / "overrides"
        self.overrides_dir.mkdir(parents=True, exist_ok=True)

    def _get_override_path(self, knowledge_id: str, project_id: str) -> Path:
        """Resolve override file path safely.

        Returns: Path (validated)
        """
        project_dir = self.overrides_dir / project_id
        filename = f"{knowledge_id}.yaml"
        file_path = project_dir / filename

        # Path traversal prevention
        try:
            resolved = file_path.resolve()
            project_resolved = project_dir.resolve()
            if not str(resolved).startswith(str(project_resolved)):
                raise ValueError(f"Path escapes boundary")
        except Exception as e:
            raise ValueError(f"Invalid path: {e}")

        return file_path

    def load_override(
        self, knowledge_id: str, project_id: str
    ) -> Tuple[bool, Optional[ProjectOverride], str]:
        """Load project override.

        Returns: (success, override, error_message)
        """
        file_path = self._get_override_path(knowledge_id, project_id)

        if not file_path.exists():
            return False, None, f"Override not found: {project_id}/{knowledge_id}"

        # Load YAML safely
        success, data, error = DataSecurityValidator.safe_yaml_load(file_path)
        if not success:
            return False, None, error

        # Validate schema
        try:
            override = ProjectOverride(**data)
            return True, override, ""
        except Exception as e:
            return False, None, f"Schema validation error: {e}"

    def save_override(
        self, override: ProjectOverride, project_id: str
    ) -> Tuple[bool, str]:
        """Save project override.

        Returns: (success, error_message)
        """
        # Validate override
        try:
            ProjectOverride(**override.dict())
        except Exception as e:
            return False, f"Override validation failed: {e}"

        # Create project directory
        project_dir = self.overrides_dir / project_id
        project_dir.mkdir(parents=True, exist_ok=True)

        file_path = self._get_override_path(override.metadata.id, project_id)

        # Save to YAML
        try:
            data = override.model_dump()
            success, error = DataSecurityValidator.safe_yaml_dump(data, file_path)
            if not success:
                return False, error

            # Set permissions (project-specific)
            os.chmod(file_path, 0o640)
            return True, ""
        except Exception as e:
            return False, f"Error saving override: {e}"

    def delete_override(self, knowledge_id: str, project_id: str) -> Tuple[bool, str]:
        """Delete a project override.

        Returns: (success, error_message)
        """
        file_path = self._get_override_path(knowledge_id, project_id)

        if not file_path.exists():
            return False, f"Override not found: {project_id}/{knowledge_id}"

        try:
            os.chmod(file_path, 0o640)
            file_path.unlink()
            return True, ""
        except Exception as e:
            return False, f"Error deleting override: {e}"

    def list_overrides_for_project(self, project_id: str) -> list[str]:
        """List all overrides for a project.

        Returns: list of knowledge IDs
        """
        project_dir = self.overrides_dir / project_id
        if not project_dir.exists():
            return []

        ids = []
        for file_path in project_dir.glob("*.yaml"):
            ids.append(file_path.stem)
        return sorted(ids)

    def list_projects(self) -> list[str]:
        """List all projects with overrides.

        Returns: list of project IDs
        """
        projects = []
        for item in self.overrides_dir.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                projects.append(item.name)
        return sorted(projects)

    def compose(
        self, master: KnowledgeRecord, override: ProjectOverride
    ) -> dict:
        """Compose master + override into effective knowledge.

        Returns: composed knowledge dict (not persisted)
        """
        # Composition logic from APP-SPEC.md Section 6
        composed = {
            "metadata": {
                **master.metadata.model_dump(),
                "id": override.metadata.id,
                "version": override.metadata.version,
                "scope": "project_override",
            },
            "content": {
                "title": override.content.title or master.content.title,
                "summary": override.content.summary or master.content.summary,
                "requirements": (
                    override.content.requirements or master.content.requirements
                ),
                "checks": override.content.checks or master.content.checks,
            },
            "source": {
                "master_sources": master.source.sources,
                "override_sources": override.source.sources,
                "applied_source_type": override.source.primary_source_type,
                "evidence_sufficiency": override.source.evidence_sufficiency,
            },
            "approval": {
                "master_approval": master.approval.model_dump(),
                "override_approval": override.approval.model_dump(),
                "effective_approval": override.approval.model_dump(),
            },
        }
        return composed
