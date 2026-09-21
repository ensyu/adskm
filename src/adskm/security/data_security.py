"""General data security (YAML, input validation, path traversal)."""
import os
import yaml
from pathlib import Path
from typing import Any


class DataSecurityValidator:
    """Validate data security (injection, traversal, credential leakage)."""

    MAX_YAML_SIZE = 1_000_000  # 1 MB

    @staticmethod
    def check_yaml_size(file_path: Path) -> tuple[bool, str]:
        """Reject oversized YAML files (DoS prevention).

        Returns: (is_safe, error_message)
        """
        try:
            size = os.path.getsize(file_path)
            if size > DataSecurityValidator.MAX_YAML_SIZE:
                return (
                    False,
                    f"YAML file {size} bytes exceeds {DataSecurityValidator.MAX_YAML_SIZE} limit",
                )
        except OSError as e:
            return False, f"Cannot read file size: {e}"

        return True, ""

    @staticmethod
    def safe_yaml_load(file_path: Path) -> tuple[bool, Any, str]:
        """Load YAML safely using yaml.safe_load only.

        Returns: (success, data, error_message)
        """
        # Check size first
        size_ok, size_error = DataSecurityValidator.check_yaml_size(file_path)
        if not size_ok:
            return False, None, size_error

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                # CRITICAL: NEVER use yaml.load() - only safe_load()
                data = yaml.safe_load(f)
                return True, data, ""
        except yaml.YAMLError as e:
            return False, None, f"YAML parse error: {e}"
        except UnicodeDecodeError as e:
            return False, None, f"Invalid UTF-8 encoding: {e}"
        except Exception as e:
            return False, None, f"Error loading YAML: {e}"

    @staticmethod
    def safe_yaml_dump(data: dict, file_path: Path) -> tuple[bool, str]:
        """Dump data to YAML safely.

        Returns: (success, error_message)
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)
                return True, ""
        except Exception as e:
            return False, f"Error writing YAML: {e}"

    @staticmethod
    def check_credential_leakage(data: dict) -> tuple[bool, list[str]]:
        """Detect potential credential leakage in data.

        Returns: (is_safe, concerns)
        """
        concerns = []
        credential_keywords = [
            "password",
            "api_key",
            "api_secret",
            "token",
            "credential",
            "secret",
            "username:password",
        ]

        def check_recursive(obj, path=""):
            if isinstance(obj, dict):
                for key, val in obj.items():
                    full_path = f"{path}.{key}" if path else key
                    # Check key names
                    for keyword in credential_keywords:
                        if keyword.lower() in key.lower():
                            concerns.append(
                                f"Credential-like field found: {full_path}"
                            )
                    # Check values
                    check_recursive(val, full_path)
            elif isinstance(obj, str):
                # Check for common credential patterns
                if "@" in obj and "://" in obj:
                    # URL with credentials
                    concerns.append(
                        f"URL with credentials detected at {path}"
                    )
                if obj.startswith("http://") and "password" in obj.lower():
                    concerns.append(f"HTTP URL with password at {path}")

        check_recursive(data)
        return len(concerns) == 0, concerns

    @staticmethod
    def check_personal_information(data: dict) -> tuple[bool, list[str]]:
        """Detect personal information (names, emails, phone).

        Returns: (is_safe, concerns)
        """
        concerns = []
        import re

        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        phone_pattern = r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"

        def check_recursive(obj, path=""):
            if isinstance(obj, dict):
                for key, val in obj.items():
                    full_path = f"{path}.{key}" if path else key
                    check_recursive(val, full_path)
            elif isinstance(obj, str):
                if re.search(email_pattern, obj):
                    concerns.append(f"Email address detected at {path}")
                if re.search(phone_pattern, obj):
                    concerns.append(f"Phone number detected at {path}")

        check_recursive(data)
        return len(concerns) == 0, concerns

    @staticmethod
    def check_external_api_exposure(data: dict) -> tuple[bool, list[str]]:
        """Detect exposed external API endpoints.

        Returns: (is_safe, concerns)
        """
        concerns = []
        api_keywords = ["api_endpoint", "webhook", "mcp_", "kanna_", "garoon_"]

        def check_recursive(obj, path=""):
            if isinstance(obj, dict):
                for key, val in obj.items():
                    full_path = f"{path}.{key}" if path else key
                    for keyword in api_keywords:
                        if keyword in key.lower():
                            concerns.append(
                                f"API-related field found: {full_path}"
                            )
                    check_recursive(val, full_path)
            elif isinstance(obj, str):
                if obj.startswith("http") and any(
                    api in obj for api in ["api", "kanna", "garoon", "mcp"]
                ):
                    concerns.append(f"Potential API URL at {path}")

        check_recursive(data)
        return len(concerns) == 0, concerns

    @staticmethod
    def comprehensive_data_security_check(
        file_path: Path, data: dict
    ) -> dict:
        """Comprehensive data security check.

        Returns: dict with all security checks
        """
        size_ok, size_error = DataSecurityValidator.check_yaml_size(file_path)
        cred_ok, cred_concerns = DataSecurityValidator.check_credential_leakage(
            data
        )
        pii_ok, pii_concerns = DataSecurityValidator.check_personal_information(
            data
        )
        api_ok, api_concerns = DataSecurityValidator.check_external_api_exposure(
            data
        )

        all_passed = size_ok and cred_ok and pii_ok and api_ok

        return {
            "passed": all_passed,
            "file_size": {"passed": size_ok, "error": size_error},
            "credentials": {"passed": cred_ok, "concerns": cred_concerns},
            "pii": {"passed": pii_ok, "concerns": pii_concerns},
            "api_exposure": {"passed": api_ok, "concerns": api_concerns},
            "overall_concerns": cred_concerns + pii_concerns + api_concerns,
        }
