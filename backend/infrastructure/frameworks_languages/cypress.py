"""Cypress execution strategies."""

from __future__ import annotations

import uuid

from .base import BaseExecutionStrategy
from .runtime import build_js_runtime, discover_node_executable, strip_code_fences, strip_common_imports, strip_typescript_annotations


class _BaseCypressExecutionStrategy(BaseExecutionStrategy):
    framework_name = "cypress"
    default_language = "javascript"

    def build_command(self, file_path: str, language: str | None = None, temp_dir: str | None = None) -> list[str]:
        node_executable = discover_node_executable()
        return [node_executable or self._python_command(), file_path]

    def normalize_script(self, script: str, language: str | None = None) -> str:
        cleaned = strip_code_fences(script)
        cleaned = strip_common_imports(cleaned)
        if (language or "").lower() == "typescript":
            cleaned = strip_typescript_annotations(cleaned)
        return build_js_runtime(cleaned, mode="cypress", browser_headless=True)


class CypressJavaScriptExecutionStrategy(_BaseCypressExecutionStrategy):
    supported_languages = ("javascript",)

    def determine_filename(self, framework: str, script: str, language: str | None = None) -> str:
        return f"test_{uuid.uuid4().hex}.js"


class CypressTypeScriptExecutionStrategy(_BaseCypressExecutionStrategy):
    supported_languages = ("typescript",)
    default_language = "typescript"

    def determine_filename(self, framework: str, script: str, language: str | None = None) -> str:
        return f"test_{uuid.uuid4().hex}.ts"
