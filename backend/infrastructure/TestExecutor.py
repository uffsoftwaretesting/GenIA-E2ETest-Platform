"""Generic sandboxed test execution for generated scripts."""

from __future__ import annotations

from typing import Callable, Optional

from backend.domain.models import ExecutionResult
from backend.infrastructure.frameworks_languages import ExecutionStrategyRegistry, get_execution_strategy


class TestExecutor:
    def __init__(self, registry: ExecutionStrategyRegistry | None = None) -> None:
        self._registry = registry or ExecutionStrategyRegistry()

    def resolve_strategy(self, framework: str, language: str | None = None, script: str | None = None):
        return self._registry.resolve(framework, language, script)

    def execute(
        self,
        framework: str,
        script: str,
        language: str | None = None,
        log_callback: Optional[Callable[[str, str], None]] = None,
    ) -> ExecutionResult:
        strategy = self.resolve_strategy(framework, language, script)
        return strategy.execute(framework, script, language=language, log_callback=log_callback)


__all__ = ["TestExecutor", "get_execution_strategy"]
