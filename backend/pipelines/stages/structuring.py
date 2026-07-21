"""Structuring stage."""

from __future__ import annotations

from typing import Any, List

from backend.domain.models import TestCase

from .base import PipelineStageRunner
from ..shared import _append_context_block, _render_prompt


class StructuringStage(PipelineStageRunner):
    async def run(
        self,
        current_api_key: str,
        current_model: str,
        current_provider: str,
        current_temperature: float,
        test_case: str,
        input_mode: str = "test_case",
        user_story_content: str | None = None,
        user_story_filename: str | None = None,
        manual_urls: List[str] | None = None,
        prompt_override: str | None = None,
        temperature: float | None = None,
        llm_override: dict[str, Any] | None = None,
    ) -> TestCase:
        provider, model, api_key, resolved_temperature = self.resolve_stage_llm(
            current_provider,
            current_model,
            current_api_key,
            current_temperature,
            "structuring",
            {"structuring": llm_override} if llm_override else None,
        )
        return await self.execute(
            test_case,
            api_key,
            model,
            provider,
            temperature=temperature if temperature is not None else resolved_temperature,
            input_mode=input_mode,
            user_story_content=user_story_content,
            user_story_filename=user_story_filename,
            manual_urls=manual_urls,
            prompt_override=prompt_override,
        )

    async def execute(
        self,
        test_case: str,
        api_key: str,
        model: str,
        provider: str,
        temperature: float = 0.0,
        input_mode: str = "test_case",
        user_story_content: str | None = None,
        user_story_filename: str | None = None,
        manual_urls: List[str] | None = None,
        prompt_override: str | None = None,
    ) -> TestCase:
        del provider
        prompt_key = "structuring_user_history" if input_mode == "user_story" else "structuring"
        prompt = prompt_override or self.prompt_manager.load_prompt(prompt_key)
        final_prompt = _append_context_block(
            _render_prompt(
                prompt,
                test_case=test_case,
                input_mode=input_mode,
                user_story_content=user_story_content or "",
                user_story_filename=user_story_filename or "",
                manual_urls=manual_urls or [],
            ),
            {
                "test_case": test_case,
                "input_mode": input_mode,
                "user_story_content": user_story_content or "",
                "user_story_filename": user_story_filename or "",
                "manual_urls": manual_urls or [],
            },
        )
        result = self.llm.generate_json(api_key, model, final_prompt, temperature=temperature)
        return TestCase(**result)


__all__ = ["StructuringStage"]
