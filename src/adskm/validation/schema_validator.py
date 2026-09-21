"""Schema and format validation."""
import re
from pathlib import Path
from ..models import KnowledgeRecord, ProjectOverride


class SchemaValidator:
    """Validate knowledge records against Pydantic schema."""

    @staticmethod
    def validate_knowledge_record(data: dict) -> tuple[bool, list[str]]:
        """Validate knowledge record data against schema.

        Returns: (is_valid, errors)
        """
        errors = []

        try:
            KnowledgeRecord(**data)
            return True, []
        except Exception as e:
            errors.append(str(e))
            return False, errors

    @staticmethod
    def validate_project_override(data: dict) -> tuple[bool, list[str]]:
        """Validate project override data against schema.

        Returns: (is_valid, errors)
        """
        errors = []

        try:
            ProjectOverride(**data)
            return True, []
        except Exception as e:
            errors.append(str(e))
            return False, errors

    @staticmethod
    def validate_knowledge_id_format(knowledge_id: str) -> tuple[bool, str]:
        """Validate knowledge ID format: KNW-[A-Z0-9]{3}-[A-Z0-9]{3}-[0-9]{3}.

        Returns: (is_valid, error_message)
        """
        pattern = r"^KNW-[A-Z0-9]{3}-[A-Z0-9]{3}-[0-9]{3}$"
        if re.match(pattern, knowledge_id):
            return True, ""

        return (
            False,
            f"Knowledge ID '{knowledge_id}' does not match format KNW-XXX-XXX-###",
        )

    @staticmethod
    def validate_no_path_traversal(path_component: str) -> tuple[bool, str]:
        """Reject path traversal patterns in identifiers.

        Returns: (is_safe, error_message)
        """
        forbidden = ["..", "/", "\\", "~"]
        for pattern in forbidden:
            if pattern in path_component:
                return False, f"Path traversal character '{pattern}' not allowed"

        return True, ""

    @staticmethod
    def check_symlink_safety(file_path: Path) -> tuple[bool, str]:
        """Check for symlinks in path components BEFORE resolution.

        Returns: (is_safe, error_message)
        """
        path_obj = Path(file_path)
        current = Path(".")

        try:
            for component in path_obj.parts:
                current = current / component
                if current.is_symlink():
                    return False, f"Path component is symlink: {component}"
        except Exception as e:
            return False, f"Error checking symlinks: {e}"

        return True, ""

    @staticmethod
    def check_path_boundary(file_path: Path, base_dir: Path) -> tuple[bool, str]:
        """Verify resolved path stays within base directory.

        Returns: (is_safe, error_message)
        """
        try:
            resolved = file_path.resolve()
            base_resolved = base_dir.resolve()

            if not str(resolved).startswith(str(base_resolved)):
                return False, f"Path escapes boundary: {file_path}"
        except Exception as e:
            return False, f"Error resolving path: {e}"

        return True, ""

    @staticmethod
    def validate_version_format(version: str) -> tuple[bool, str]:
        """Validate semantic version format: MAJOR.MINOR.PATCH.

        Returns: (is_valid, error_message)
        """
        pattern = r"^\d+\.\d+\.\d+$"
        if re.match(pattern, version):
            return True, ""

        return False, f"Version '{version}' does not match semantic versioning"

    @staticmethod
    def validate_iso8601_datetime(datetime_str: str) -> tuple[bool, str]:
        """Validate ISO 8601 datetime format.

        Returns: (is_valid, error_message)
        """
        pattern = (
            r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$"
        )
        if re.match(pattern, datetime_str):
            return True, ""

        return False, f"Datetime '{datetime_str}' does not match ISO 8601 format"

    @staticmethod
    def validate_field_length_limits(record: dict) -> tuple[bool, list[str]]:
        """Validate field length limits.

        Returns: (is_valid, violations)
        """
        violations = []
        limits = {
            ("metadata", "building_type"): 64,
            ("content", "title"): 100,
            ("content", "summary"): 500,
            ("source", "evidence_notes"): 5000,
            ("approval", "approval_comment"): 2000,
        }

        for path, max_len in limits.items():
            value = record
            try:
                for key in path:
                    value = value.get(key, {}) if isinstance(value, dict) else {}
                if isinstance(value, str) and len(value) > max_len:
                    violations.append(
                        f"{'.'.join(path)}: {len(value)} chars exceeds {max_len}"
                    )
            except (AttributeError, TypeError):
                pass

        return len(violations) == 0, violations
