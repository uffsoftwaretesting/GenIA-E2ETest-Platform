"""Strategy registry for framework/language execution."""

from __future__ import annotations

from functools import lru_cache

from .base import BaseExecutionStrategy, GenericPythonExecutionStrategy
from .cypress import CypressJavaScriptExecutionStrategy, CypressTypeScriptExecutionStrategy
from .junit import JUnitJavaExecutionStrategy
from .playwright import PlaywrightJavaScriptExecutionStrategy, PlaywrightTypeScriptExecutionStrategy
from .pytest import PytestPythonExecutionStrategy
from .robotframework import RobotFrameworkPythonExecutionStrategy
from .selenium import (
    SeleniumJavaExecutionStrategy,
    SeleniumJavaScriptExecutionStrategy,
    SeleniumPythonExecutionStrategy,
    SeleniumTypeScriptExecutionStrategy,
)


class ExecutionStrategyRegistry:
    def __init__(self) -> None:
        self._strategies: tuple[BaseExecutionStrategy, ...] = (
            RobotFrameworkPythonExecutionStrategy(),
            PlaywrightJavaScriptExecutionStrategy(),
            PlaywrightTypeScriptExecutionStrategy(),
            CypressJavaScriptExecutionStrategy(),
            CypressTypeScriptExecutionStrategy(),
            PytestPythonExecutionStrategy(),
            JUnitJavaExecutionStrategy(),
            SeleniumPythonExecutionStrategy(),
            SeleniumJavaScriptExecutionStrategy(),
            SeleniumTypeScriptExecutionStrategy(),
            SeleniumJavaExecutionStrategy(),
            GenericPythonExecutionStrategy(),
        )

    @lru_cache(maxsize=1)
    def _mapping(self) -> dict[tuple[str, str], BaseExecutionStrategy]:
        mapping: dict[tuple[str, str], BaseExecutionStrategy] = {}
        for strategy in self._strategies:
            framework = strategy.framework_name.lower()
            for language in strategy.supported_languages:
                mapping[(framework, language.lower())] = strategy
        return mapping

    def resolve(self, framework: str, language: str | None = None, script: str | None = None) -> BaseExecutionStrategy:
        normalized_framework = (framework or "").lower()
        normalized_language = (language or "").lower()
        mapping = self._mapping()

        if (normalized_framework, normalized_language) in mapping:
            return mapping[(normalized_framework, normalized_language)]

        if normalized_framework == "selenium":
            if not normalized_language and script:
                lowered_script = script.lower()
                if "public class" in lowered_script or "@test" in lowered_script:
                    return SeleniumJavaExecutionStrategy()
                if "def test_" in lowered_script or "pytest" in lowered_script:
                    return SeleniumPythonExecutionStrategy()
                if "import { test" in lowered_script or "describe(" in lowered_script or "cy." in lowered_script:
                    return SeleniumJavaScriptExecutionStrategy()
            if normalized_language == "python":
                return SeleniumPythonExecutionStrategy()
            if normalized_language == "javascript":
                return SeleniumJavaScriptExecutionStrategy()
            if normalized_language == "typescript":
                return SeleniumTypeScriptExecutionStrategy()
            if normalized_language == "java":
                return SeleniumJavaExecutionStrategy()

        if normalized_framework == "playwright":
            return PlaywrightTypeScriptExecutionStrategy() if normalized_language == "typescript" else PlaywrightJavaScriptExecutionStrategy()

        if normalized_framework == "cypress":
            return CypressTypeScriptExecutionStrategy() if normalized_language == "typescript" else CypressJavaScriptExecutionStrategy()

        if normalized_framework == "junit":
            return JUnitJavaExecutionStrategy()

        if normalized_framework == "pytest":
            return PytestPythonExecutionStrategy()

        if normalized_framework == "robotframework":
            return RobotFrameworkPythonExecutionStrategy()

        if normalized_framework == "python":
            return GenericPythonExecutionStrategy()

        return GenericPythonExecutionStrategy()
