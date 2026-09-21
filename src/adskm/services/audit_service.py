"""Audit Service - Append-only audit logging with file locking."""
import os
import time
import threading
from pathlib import Path
from datetime import datetime
from typing import Tuple, List
import yaml
from ..models import AuditEntry


class AuditWriteError(Exception):
    """Raised when audit log write fails after retries."""

    pass


class AuditService:
    """Manage append-only audit logs with concurrent write protection."""

    def __init__(self, audit_dir: Path):
        """Initialize audit service.

        Args:
            audit_dir: Path to audit_logs/ directory
        """
        self.audit_dir = Path(audit_dir)
        self.archive_dir = self.audit_dir / "archive"
        self.audit_file = self.audit_dir / "audit.yaml"
        self.max_audit_size = 10_000_000  # 10 MB
        self.max_retries = 5
        self.backoff_ms = [100, 200, 400, 800, 1600]

        # Per-file mutex for concurrent write safety (single process)
        self._locks = {}

        # Create directories
        self.audit_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)

        # Initialize audit file if needed
        if not self.audit_file.exists():
            self.audit_file.touch()

    def _get_lock(self, file_path: Path) -> threading.Lock:
        """Get or create mutex for file."""
        path_str = str(file_path)
        if path_str not in self._locks:
            self._locks[path_str] = threading.Lock()
        return self._locks[path_str]

    def _rotate_if_needed(self) -> Tuple[bool, str]:
        """Rotate audit log if it exceeds size limit.

        Returns: (rotated, error_message)
        """
        try:
            size = os.path.getsize(self.audit_file)
            if size >= self.max_audit_size:
                # Rotate
                timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                archive_path = self.archive_dir / f"AUD_{timestamp}.yaml"

                os.rename(self.audit_file, archive_path)
                os.chmod(archive_path, 0o444)  # Read-only

                # Create new audit file
                self.audit_file.touch()
                return True, ""
        except Exception as e:
            return False, f"Rotation failed: {e}"

        return False, ""

    def append_entry(self, entry: AuditEntry) -> Tuple[bool, str]:
        """Append audit entry to log (safe append with locking).

        Returns: (success, error_message)
        """
        lock = self._get_lock(self.audit_file)

        for attempt in range(self.max_retries):
            try:
                with lock:
                    # Check rotation need
                    rotated, rotate_error = self._rotate_if_needed()
                    if rotated and rotate_error:
                        return False, rotate_error

                    # Append entry
                    with open(self.audit_file, "a", encoding="utf-8") as f:
                        # YAML stream separator
                        f.write("---\n")
                        # Write single entry (not list)
                        yaml.safe_dump(
                            entry.model_dump(),
                            f,
                            default_flow_style=False,
                            sort_keys=False,
                        )
                    return True, ""

            except IOError as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.backoff_ms[attempt] / 1000.0)
                else:
                    return (
                        False,
                        f"Failed to acquire audit lock after {self.max_retries} retries: {e}",
                    )
            except Exception as e:
                return False, f"Audit write error: {e}"

        return False, "Unknown audit write error"

    def read_all_entries(self) -> Tuple[bool, List[AuditEntry], str]:
        """Read all audit entries from all files.

        Returns: (success, entries, error_message)
        """
        entries = []

        # Read main audit file
        if self.audit_file.exists():
            success, entry_list, error = self._read_file(self.audit_file)
            if not success:
                return False, [], error
            entries.extend(entry_list)

        # Read archived audit files (sorted by date)
        archive_files = sorted(self.archive_dir.glob("AUD_*.yaml"))
        for archive_file in archive_files:
            success, entry_list, error = self._read_file(archive_file)
            if not success:
                return False, [], error
            entries.extend(entry_list)

        return True, sorted(entries, key=lambda e: e.timestamp), ""

    def _read_file(self, file_path: Path) -> Tuple[bool, List[AuditEntry], str]:
        """Read audit entries from single file.

        Returns: (success, entries, error_message)
        """
        entries = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Split on YAML stream separator
            if not content.strip():
                return True, [], ""

            blocks = content.split("---\n")
            for block in blocks:
                if not block.strip():
                    continue

                try:
                    data = yaml.safe_load(block)
                    if data:
                        entry = AuditEntry(**data)
                        entries.append(entry)
                except Exception as e:
                    return False, [], f"Parse error in {file_path}: {e}"

            return True, entries, ""

        except Exception as e:
            return False, [], f"Error reading audit file: {e}"

    def query_entries(
        self, knowledge_id: str = None, action: str = None
    ) -> Tuple[bool, List[AuditEntry], str]:
        """Query audit entries by knowledge_id or action.

        Returns: (success, entries, error_message)
        """
        success, all_entries, error = self.read_all_entries()
        if not success:
            return False, [], error

        filtered = all_entries

        if knowledge_id:
            filtered = [e for e in filtered if e.knowledge_id == knowledge_id]

        if action:
            filtered = [e for e in filtered if e.action == action]

        return True, filtered, ""

    def get_last_entry_for_knowledge(self, knowledge_id: str) -> Tuple[bool, AuditEntry, str]:
        """Get most recent audit entry for knowledge ID.

        Returns: (success, entry, error_message)
        """
        success, entries, error = self.query_entries(knowledge_id=knowledge_id)
        if not success:
            return False, None, error

        if not entries:
            return False, None, f"No audit entries found for {knowledge_id}"

        return True, entries[-1], ""
