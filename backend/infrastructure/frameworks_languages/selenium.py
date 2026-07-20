"""Selenium execution strategies."""

from __future__ import annotations

import uuid

from .base import BaseExecutionStrategy
from .runtime import (
    build_js_runtime,
    discover_node_executable,
    extract_async_iife_body,
    strip_code_fences,
    strip_common_imports,
    strip_typescript_annotations,
    translate_java_source_to_js,
)


class _BaseSeleniumExecutionStrategy(BaseExecutionStrategy):
    framework_name = "selenium"

    def build_command(self, file_path: str, language: str | None = None, temp_dir: str | None = None) -> list[str]:
        node_executable = discover_node_executable()
        return [node_executable or self._python_command(), file_path]

    def normalize_script(self, script: str, language: str | None = None) -> str:
        cleaned = strip_code_fences(script)
        cleaned = strip_common_imports(cleaned)
        if (language or "").lower() == "typescript":
            cleaned = strip_typescript_annotations(cleaned)
        extracted = extract_async_iife_body(cleaned)
        if extracted:
            cleaned = extracted
        return build_js_runtime(cleaned, mode="selenium", browser_headless=True)


class SeleniumPythonExecutionStrategy(_BaseSeleniumExecutionStrategy):
    supported_languages = ("python",)
    default_language = "python"

    def determine_filename(self, framework: str, script: str, language: str | None = None) -> str:
        return f"test_{uuid.uuid4().hex}.py"

    def build_command(self, file_path: str, language: str | None = None, temp_dir: str | None = None) -> list[str]:
        return self._pytest_command(file_path)


class SeleniumJavaScriptExecutionStrategy(_BaseSeleniumExecutionStrategy):
    supported_languages = ("javascript",)
    default_language = "javascript"

    def determine_filename(self, framework: str, script: str, language: str | None = None) -> str:
        return f"test_{uuid.uuid4().hex}.js"

    def build_command(self, file_path: str, language: str | None = None, temp_dir: str | None = None) -> list[str]:
        return super().build_command(file_path, language, temp_dir)


class SeleniumTypeScriptExecutionStrategy(_BaseSeleniumExecutionStrategy):
    supported_languages = ("typescript",)
    default_language = "typescript"

    def determine_filename(self, framework: str, script: str, language: str | None = None) -> str:
        return f"test_{uuid.uuid4().hex}.ts"

    def build_command(self, file_path: str, language: str | None = None, temp_dir: str | None = None) -> list[str]:
        return super().build_command(file_path, language, temp_dir)


class SeleniumJavaExecutionStrategy(_BaseSeleniumExecutionStrategy):
    supported_languages = ("java",)
    default_language = "java"

    def determine_filename(self, framework: str, script: str, language: str | None = None) -> str:
        return "GeneratedTest.java"

    def normalize_script(self, script: str, language: str | None = None) -> str:
        if (language or "").lower() == "java":
            combined = translate_java_source_to_js(script)
            return build_js_runtime(combined, mode="java", browser_headless=True)

        cleaned = strip_code_fences(script)
        cleaned = strip_common_imports(cleaned)
        if (language or "").lower() == "typescript":
            cleaned = strip_typescript_annotations(cleaned)
        extracted = extract_async_iife_body(cleaned)
        if extracted:
            cleaned = extracted
        return build_js_runtime(cleaned, mode="selenium", browser_headless=True)
