"""Confirmation stage."""

from __future__ import annotations

from typing import Any, Dict

from .base import PipelineStageRunner
from ..shared import _append_context_block, _render_prompt


class ConfirmationStage(PipelineStageRunner):
    async def run(
        self,
        current_provider: str,
        current_model: str,
        current_api_key: str,
        current_temperature: float,
        refined_script: str,
        manual_changes: Dict[str, Any],
        temperature: float | None = None,
        prompt_override: str | None = None,
        llm_override: Dict[str, Any] | None = None,
    ) -> str:
        provider, model, api_key, resolved_temperature = self.resolve_stage_llm(
            current_provider,
            current_model,
            current_api_key,
            current_temperature,
            "confirmation",
            {"confirmation": llm_override} if llm_override else None,
        )
        return await self.execute(
            refined_script,
            manual_changes,
            api_key,
            model,
            provider,
            temperature=temperature if temperature is not None else resolved_temperature,
            prompt_override=prompt_override,
        )

    async def execute(
        self,
        script: str,
        manual_changes: Dict[str, Any],
        api_key: str,
        model: str,
        provider: str,
        temperature: float = 0.0,
        prompt_override: str | None = None,
    ) -> str:
        del provider
        prompt = prompt_override or self.prompt_manager.load_prompt("confirmation")
        final_prompt = _append_context_block(
            _render_prompt(
                prompt,
                refined_test=script,
                generation_script=script,
                manual_inputs=manual_changes,
                validation_changes=manual_changes,
                manual_changes=manual_changes,
                confirmation_context={
                    "script": script,
                    "manual_changes": manual_changes,
                },
            ),
            {
                "script": script,
                "manual_changes": manual_changes,
                "generation_script": script,
                "validation_changes": manual_changes,
            },
        )
        return self.llm.generate_text(api_key, model, final_prompt, temperature=temperature)


__all__ = ["ConfirmationStage"]
