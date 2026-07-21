"""Homologation stage."""

from __future__ import annotations

from typing import Any, Dict

from backend.domain.models import ExecutionResult

from .base import PipelineStageRunner
from ..shared import _append_context_block, _compact_execution_artifacts, _json_safe, _render_prompt


class HomologationStage(PipelineStageRunner):
    async def run(
        self,
        current_provider: str,
        current_model: str,
        current_api_key: str,
        current_temperature: float,
        execution_result: ExecutionResult,
        refined: Any,
        validation_data: Dict[str, Any],
        manual_changes: Dict[str, Any],
        script: str,
        temperature: float | None = None,
        prompt_override: str | None = None,
        llm_override: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        provider, model, api_key, resolved_temperature = self.resolve_stage_llm(
            current_provider,
            current_model,
            current_api_key,
            current_temperature,
            "homologation",
            {"homologation": llm_override} if llm_override else None,
        )
        return await self.execute(
            execution_result,
            refined,
            validation_data,
            manual_changes,
            script,
            api_key,
            model,
            provider,
            temperature=temperature if temperature is not None else resolved_temperature,
            prompt_override=prompt_override,
        )

    async def execute(
        self,
        execution_result: ExecutionResult,
        refined: Any,
        validation_data: Dict[str, Any],
        manual_changes: Dict[str, Any],
        script: str,
        api_key: str,
        model: str,
        provider: str,
        temperature: float = 0.0,
        prompt_override: str | None = None,
    ) -> Dict[str, Any]:
        del provider
        prompt = prompt_override or self.prompt_manager.load_prompt("homologation")
        visual_context = _compact_execution_artifacts(execution_result)
        final_prompt = _append_context_block(
            _render_prompt(
                prompt,
                execution_results=execution_result,
                execution=execution_result,
                execution_screenshots=visual_context.get("screenshots"),
                primary_screenshot=visual_context.get("primary_screenshot"),
                image_evidence=visual_context.get("image_evidence"),
                refined_data=refined,
                refined=refined,
                validation_data=validation_data,
                manual_changes=manual_changes,
                manual=manual_changes,
                generated_script=script,
                script=script,
                homologation_context={
                    "execution_result": execution_result,
                    "visual_context": visual_context,
                    "refined": refined,
                    "validation": validation_data,
                    "manual_changes": manual_changes,
                    "script": script,
                },
            ),
            {
                "execution_results": execution_result,
                "execution_screenshots": visual_context.get("screenshots"),
                "primary_screenshot": visual_context.get("primary_screenshot"),
                "image_evidence": visual_context.get("image_evidence"),
                "refined_data": refined,
                "validation_data": validation_data,
                "manual_changes": manual_changes,
                "generated_script": script,
            },
        )
        result = self.llm.generate_json(api_key, model, final_prompt, temperature=temperature)
        return _json_safe(result)


__all__ = ["HomologationStage"]
