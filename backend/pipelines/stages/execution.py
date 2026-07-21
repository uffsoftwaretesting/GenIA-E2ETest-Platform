"""Execution stage."""

from __future__ import annotations

from typing import Callable, Optional

from backend.domain.models import ExecutionResult

from .base import PipelineStageRunner


class ExecutionStage(PipelineStageRunner):
    async def run(
        self,
        script: str,
        framework: str,
        language: str,
        log_callback: Optional[Callable[[str, str], None]] = None,
    ) -> ExecutionResult:
        return await self.execute(script, framework, language, log_callback=log_callback)

    async def execute(
        self,
        script: str,
        framework: str,
        language: str,
        log_callback: Optional[Callable[[str, str], None]] = None,
    ) -> ExecutionResult:
        from backend.infrastructure.TestExecutor import TestExecutor

        return TestExecutor().execute(framework, script, language=language, log_callback=log_callback)


__all__ = ["ExecutionStage"]
