"""Refactoring stage."""

from __future__ import annotations

from typing import Any, Dict

from backend.domain.models import ExecutionResult

from .base import PipelineStageRunner
from ..shared import _append_context_block, _compact_execution_artifacts, _json_safe, _render_prompt


class RefactoringStage(PipelineStageRunner):
    async def run(
        self,
        current_provider: str,
        current_model: str,
        current_api_key: str,
        current_temperature: float,
        original_script: str,
        execution_result: ExecutionResult,
        homologation: Dict[str, Any],
        final_report: Dict[str, Any],
        temperature: float | None = None,
        prompt_override: str | None = None,
        llm_override: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        provider, model, api_key, resolved_temperature = self.resolve_stage_llm(
            current_provider,
            current_model,
            current_api_key,
            current_temperature,
            "refactoring",
            {"refactoring": llm_override} if llm_override else None,
        )
        return await self.execute(
            original_script,
            execution_result,
            homologation,
            final_report,
            api_key,
            model,
            provider,
            temperature=temperature if temperature is not None else resolved_temperature,
            prompt_override=prompt_override,
        )

    async def execute(
        self,
        original_script: str,
        execution_result: ExecutionResult,
        homologation: Dict[str, Any],
        final_report: Dict[str, Any],
        api_key: str,
        model: str,
        provider: str,
        temperature: float = 0.0,
        prompt_override: str | None = None,
    ) -> Dict[str, Any]:
        del provider
        prompt = prompt_override or self.prompt_manager.load_prompt("refactoring")
        execution_artifacts = _compact_execution_artifacts(execution_result)
        confirmed_script = (
            final_report.get("script", {}).get("confirmed", original_script)
            if isinstance(final_report, dict)
            else original_script
        )
        final_prompt = _append_context_block(
            _render_prompt(
                prompt,
                original_script=original_script,
                script=original_script,
                confirmed_script=confirmed_script,
                execution_results=execution_result,
                execution=execution_result,
                execution_screenshots=execution_artifacts.get("screenshots"),
                primary_screenshot=execution_artifacts.get("primary_screenshot"),
                image_evidence=execution_artifacts.get("image_evidence"),
                homologation_results=homologation,
                homologation=homologation,
                finalization_context=final_report,
                final_report=final_report,
                refactoring_context={
                    "original_script": original_script,
                    "confirmed_script": confirmed_script,
                    "execution_result": execution_result,
                    "visual_context": execution_artifacts,
                    "homologation": homologation,
                    "final_report": final_report,
                },
            ),
            {
                "original_script": original_script,
                "confirmed_script": confirmed_script,
                "execution_result": execution_result,
                "execution_screenshots": execution_artifacts.get("screenshots"),
                "primary_screenshot": execution_artifacts.get("primary_screenshot"),
                "image_evidence": execution_artifacts.get("image_evidence"),
                "homologation": homologation,
                "final_report": final_report,
            },
        )
        result = self.llm.generate_json(api_key, model, final_prompt, temperature=temperature)
        return _json_safe(result)


__all__ = ["RefactoringStage"]
