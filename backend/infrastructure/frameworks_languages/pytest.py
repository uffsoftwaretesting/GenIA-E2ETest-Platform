"""Pytest execution strategy."""

from __future__ import annotations

import uuid

from .base import BaseExecutionStrategy


class PytestPythonExecutionStrategy(BaseExecutionStrategy):
    framework_name = "pytest"
    supported_languages = ("python",)
    default_language = "python"

    def determine_filename(self, framework: str, script: str, language: str | None = None) -> str:
        return f"test_{uuid.uuid4().hex}.py"

    def build_command(self, file_path: str, language: str | None = None, temp_dir: str | None = None) -> list[str]:
        return self._pytest_command(file_path)
